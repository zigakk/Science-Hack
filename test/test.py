from scipy.signal import firwin, remez, kaiser_atten, kaiser_beta

# Several flavors of bandpass FIR filters.

def bandpass_firwin(ntaps, lowcut, highcut, fs, window='hamming'):
    nyq = 0.5 * fs
    taps = firwin(ntaps, [lowcut, highcut], nyq=nyq, pass_zero=False,
                  window=window, scale=False)
    return taps

def bandpass_kaiser(ntaps, lowcut, highcut, fs, width):
    nyq = 0.5 * fs
    atten = kaiser_atten(ntaps, width / nyq)
    beta = kaiser_beta(atten)
    taps = firwin(ntaps, [lowcut, highcut], nyq=nyq, pass_zero=False,
                  window=('kaiser', beta), scale=False)
    return taps

def bandpass_remez(ntaps, lowcut, highcut, fs, width):
    delta = 0.5 * width
    edges = [0, lowcut - delta, lowcut + delta,
             highcut - delta, highcut + delta, 0.5*fs]
    taps = remez(ntaps, edges, [0, 1, 0], Hz=fs)
    return taps


if __name__ == "__main__":
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.signal import freqz, lfilter, butter, firwin, convolve, correlate
    from scipy.fftpack import fft
    import wave
    import sys    

    # Sample rate and desired cutoff frequencies (in Hz).
    fs = 44000
    lowcut = 18000
    highcut = 19000

    ntaps = 128
    taps_hamming = bandpass_firwin(ntaps, lowcut, highcut, fs=fs)
    taps_kaiser16 = bandpass_kaiser(ntaps, lowcut, highcut, fs=fs, width=1.6)
    taps_kaiser10 = bandpass_kaiser(ntaps, lowcut, highcut, fs=fs, width=1.0)
    remez_width = 1.0
    taps_remez = bandpass_remez(ntaps, lowcut, highcut, fs=fs,
                                width=remez_width)

    # Plot the frequency responses of the filters.
    plt.figure(1, figsize=(12, 9))
    plt.clf()

    # First plot the desired ideal response as a green(ish) rectangle.
    rect = plt.Rectangle((lowcut, 0), highcut - lowcut, 1.0,
                         facecolor="#60ff60", alpha=0.2)
    plt.gca().add_patch(rect)

    # Plot the frequency response of each filter.
    w, h = freqz(taps_hamming, 1, worN=2000)
    plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="Hamming window")

    w, h = freqz(taps_kaiser16, 1, worN=2000)
    plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="Kaiser window, width=1.6")

    w, h = freqz(taps_kaiser10, 1, worN=2000)
    plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="Kaiser window, width=1.0")

    w, h = freqz(taps_remez, 1, worN=2000)
    plt.plot((fs * 0.5 / np.pi) * w, abs(h),
             label="Remez algorithm, width=%.1f" % remez_width)

    plt.xlim(16000, 20000)
    plt.ylim(0, 2.0)
    plt.grid(True)
    plt.legend()
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Gain')
    plt.title('Frequency response of several FIR filters, %d taps' % ntaps)

    with wave.open('zvok/desno45.wav', 'r') as desnoF:
        #Extract Raw Audio from Wav File
        signal = desnoF.readframes(-1)
        signal = np.fromstring(signal, 'Int16')

        #Split the data into channels 
        channels = [[] for channel in range(desnoF.getnchannels())]
        for index, datum in enumerate(signal):
            channels[index%len(channels)].append(datum)

        #Get time from indices
        fs = desnoF.getframerate()
        print("Fs:", fs)
        Time=np.linspace(0, len(signal)/len(channels)/fs, num=len(signal)/len(channels))

        #Plot
        plt.figure(2)
        plt.title('Signal Wave...')
        for channel in channels:
            plt.plot(Time, channel)

        # plt.ylim(-100,100)

        n = 101
        # Lowpass filter
        a = firwin(n, cutoff=highcut, window = 'blackmanharris', nyq=22050)
        # Highpass filter with spectral inversion
        b = - firwin(n, cutoff=lowcut, window = 'blackmanharris', nyq=22050)
        b[n//2] = b[n//2] + 1
        #Combine into a bandpass filter
        d = - (a+b); d[n//2] = d[n//2] + 1

        new_channels = []

        for i, channel in enumerate(channels):
            # b, a = butter(channel)
            # new = lfilter(d, [1], channel)
            new = convolve(channel, d, mode='same')
            new_channels.append(new)
            plt.figure(3)
            plt.plot(Time, new)

            plt.figure(4)
            new_fft = fft(new, n=fs)
            plt.plot(np.abs(new_fft))

        xcorr = correlate(new_channels[0][:100], new_channels[1][:100])
        plt.figure(5)
        plt.plot(xcorr)

        from scipy.io.wavfile import write

        input = scaled = np.int16(new/np.max(np.abs(new)) * 32767)
        write('test.wav', fs, input)

    plt.show()
