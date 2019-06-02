import tensorflow as tf

class Dense(object):
    def __init__(self, units, activation, input_dim=None):
        self._units = units
        self._input_dim = input_dim
        if activation == 'tanh':
            self._activation = tf.nn.tanh
        elif activation == 'relu':
            self._activation = tf.nn.relu
        elif activation == 'linear':
            self._activation = tf.keras.activations.linear
        else:
            raise ValueError('Illegal activation function: %s' % activation)

    @property
    def units(self):
        return self._units

    @property
    def input_dim(self):
        return self._input_dim

    @property
    def activation(self):
        return self._activation

class Sequential(object):
    def __init__(self):
        self._graph = tf.Graph()
        self._layers = []
        self._tf_layers = []

    def add(self, layer):
        if len(self._layers) == 0:
            with self._graph.as_default():
                input_dim = self._output_dim if layer.input_dim is None else layer.input_dim
                self._x = tf.placeholder(tf.float32, [None, input_dim], name="x")
            inputs = self._x
        else:
            inputs = self._tf_layers[-1]
        with self._graph.as_default():
            tf_layer = tf.contrib.layers.fully_connected(inputs=inputs, num_outputs=layer.units, activation_fn=layer.activation, scope='Layer_%s' % (len(self._layers) + 1))
        self._layers.append(layer)
        self._tf_layers.append(tf_layer)
        self._output_dim = layer.units

    def compile(self, loss, optimizer, lr=0.001):
        with self._graph.as_default():
            self._y = tf.placeholder(tf.float32, [None, self._output_dim], name="y")
        self._y_pred = self._tf_layers[-1]

        if loss == 'mean_squared_error':
            with self._graph.as_default():
                self._loss = tf.losses.mean_squared_error(labels=self._y, predictions=self._y_pred, scope='Loss_Function')
        else:
            raise ValueError('Illegal loss: %s' % loss)

        if optimizer == 'sgd':
            with self._graph.as_default():
                self._optimizer = tf.train.GradientDescentOptimizer(lr, name='Optimizer').minimize(self._loss)

    def fit(self, x, y, epochs):
        self._session = tf.InteractiveSession(graph=self._graph)
        init = tf.global_variables_initializer()
        self._session.run(init)
        for epoch in range(epochs):
            y_pred, _, loss = self._session.run([self._tf_layers[-1], self._optimizer, self._loss], feed_dict = {self._x: x, self._y: y})
        print('loss:', loss)
        return y_pred
