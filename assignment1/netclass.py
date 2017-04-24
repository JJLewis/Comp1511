import numpy as np
import openpbm
import math

class NeuralNet():

    def pMatrixDim(self, m1, n1, m2, n2):
        print n1 + " width: " + str(len(m1[0]))
        print n1 + " height: " + str(len(m1))

        print n2 + " width: " + str(len(m2[0]))
        print n2 + " height: " + str(len(m2))

    def makeGuess(self, input):
        # layers
        l0 = input
        l1 = self.nonlin(np.dot(l0, self.syn0))
        l2 = self.nonlin(np.dot(l1, self.syn1))

        return l2.tolist()

    # sigmoid function
    def nonlin(self, x, deriv=False):
        if deriv:
            return x * (1 - x)
        return 1 / (1 + np.exp(-x))

    def flattenPixels(self, pixels):
        all = []
        for i in xrange(len(pixels)):
            all += pixels[i]
        return all

    def expectedOutputFor(self, n):
        arr = [0] * 10
        arr[n] = 1
        return arr

    def loadTrainingData(self, fstruct, numnum, maxPerNum):
        import getattributeArray

        training = []
        expected = []
        for n in xrange(numnum):
            print "Loading: " + str(n)
            tempExpected = self.expectedOutputFor(n)
            for f in xrange(maxPerNum + 1):
                file = openpbm.fileNameFrom(fstruct, n, f)
                pixels = openpbm.read_pbm(file)

                inputData = getattributeArray.getAttrArr(pixels)

                training.append(inputData)
                expected.append(tempExpected)
            print "Loaded: " + str(n)
        return (np.array(training), np.array(expected))


    def train(self, numtimes, training, expected):
        for t in xrange(numtimes):
            # layers
            l0 = training
            #self.pMatrixDim(l0, 'l0', self.syn0, 'syn0')
            l1 = self.nonlin(np.dot(l0, self.syn0))
            l2 = self.nonlin(np.dot(l1, self.syn1))

            # backpropagation
            l2_error = expected - l2

            error = 'Error: ' + str(np.mean(np.abs(l2_error)))
            if t >= 10:
               if (t % (numtimes / 10)) == 0:
                  print error
            else:
                print error

            # calculate deltas
            l2_delta = l2_error * self.nonlin(l2, deriv=True)
            l1_error = l2_delta.dot(self.syn1.T)
            l1_delta = l1_error * self.nonlin(l1, deriv=True)

            # update synapses
            self.syn1 += l1.T.dot(l2_delta)
            self.syn0 += l0.T.dot(l1_delta)

    def __init__(self, numInput, numOutputNodes):
        np.random.seed(1)

        nodesInL1 = 2*numInput#int(math.ceil(((2/3.0) * numInput) + numOutputNodes))

        self.syn0 = 2 * np.random.random((numInput, nodesInL1)) - 1
        self.syn1 = 2 * np.random.random((nodesInL1, numOutputNodes)) - 1
