import tensorflow as tf
import numpy as np

data = None
vishid = None
hidrecbiases = None
numhid = None
hidpen = None
penrecbiases = None
numpen = None
pentop = None
targets = None
labtop = None
numtop = None
topbiases = None
labgenbiases = None
pengenbiases = None
hidvis = None
penhid = None
visgenbiases = None
hidgenbiases = None
r = None


wakehidprobs = tf.nn.sigmoid(data * vishid + hidrecbiases)
wakehidstates = wakehidprobs > np.rand(1, numhid)
wakepenprobs = tf.nn.sigmoid(wakehidstates * hidpen + penrecbiases)
wakepenstates = wakepenprobs > np.rand(1, numpen)
waketopprobs = tf.nn.sigmoid(wakepenstates * pentop + targets * labtop +
                            topbiases)
waketopstates = waketopprobs > np.rand(1, numtop)

poslabtopstatistics = targets.transpose * waketopstates
pospentopstatistics = wakepenstates.transpose * waketopstates

negtopstates = waketopstates

for i in range(1, 4):
    negpenprobs = tf.nn.sigmoid(negtopstates * pentop.transpose + pengenbiases)
    negpenstates = negpenprobs > np.rand(1, numpen)
    neglabprobs = tf.nn.softmax(negtopstates * labtop.transpose + labgenbiases)
    negtopprobs = tf.nn.sigmoid(negpenstates * pentop + neglabprobs * labtop +
                                topbiases)
    negtopstates = negtopprobs > np.rand(1, numtop)

negpentopstatistics = negpenstates.transpose * negtopstates
neglabtopstatistics = neglabprobs.transpose * negtopstates

sleeppenstates = negpenstates
sleephidprobs = tf.nn.sigmoid(sleeppenstates * penhid + hidgenbiases)
sleephidstates = sleephidprobs > np.rand(1, numhid)
sleepvisprobs = tf.nn.sigmoid(sleephidstates * hidvis + visgenbiases)

psleeppenstates = tf.nn.sigmoid(sleephidstates * hidpen + penrecbiases)
psleephidstates = tf.nn.sigmoid(sleepvisprobs * vishid + hidrecbiases)
pvisprobs = tf.nn.sigmoid(wakehidstates * hidvis + visgenbiases)
phidprobs = tf.nn.sigmoid(wakepenstates * penhid + hidgenbiases)

hidvis = hidvis + r * poshidstates.transpose * (data - pvisprobs) # wurde niemals deklariert

visgenbiases = visgenbiases + r * (data - pvisprobs)
penhid = penhid + r * wakepenstates.transpose * (wakehidstates - phidprobs)

labtop = labtop + r * (poslabtopstatistics - neglabtopstatistics)
labgenbiases = labgenbiases + r * (targets - neglabprobs)
pentop = pentop + r * (pospentopstatistics - negpentopstatistics)
pengenbiases = pengenbiases + r * (wakepenstates - negpenstates)
topbiases = topbiases + r * (waketopstates - negtopstates)

hidpen = hidpen + r * (sleephidstates.transpose * (sleeppenstates -
                                                   psleeppenstates))
penrecbiases = penrecbiases + r * (sleeppenstates - psleeppenstates)
vishid = vishid + r * (sleepvisprobs.transpose * (sleephidstates -
                                                  psleephidstates))
hidrecbiases = hidrecbiases + r * (sleephidstates - psleephidstates)
