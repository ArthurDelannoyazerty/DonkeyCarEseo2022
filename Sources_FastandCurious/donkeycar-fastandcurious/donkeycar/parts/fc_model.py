import os
import tensorflow as tf
import numpy as np
from typing import Dict, Union

from donkeycar.pipeline.types import TubRecord
from donkeycar.parts.keras import KerasPilot, KerasLinear, XY, core_cnn_layers
from tensorflow.keras.layers import Input, Dense, Dropout
from tensorflow.keras.backend import concatenate
from tensorflow.keras.models import Model

class KerasFCLinear(KerasPilot):
    """
    The KerasLinear pilot uses one neuron to output a continous value via the
    Keras Dense layer with linear activation. One each for steering and
    throttle. The output is not bounded.
    """
    def __init__(self, num_outputs=2, num_sensor_inputs=6, input_shape=(120, 160, 3)):
        super().__init__()
        self.num_sensor_inputs = num_sensor_inputs
        self.model = default_fc_linear(num_outputs, num_sensor_inputs, input_shape)

    def compile(self):
        self.model.compile(optimizer=self.optimizer, loss='mse')

    def inference(self, img_arr, other_arr):
        img_arr = img_arr.reshape((1,) + img_arr.shape)
        sensor_arr = np.array(other_arr).reshape(1, self.num_sensor_inputs)
        outputs = self.model.predict([img_arr, sensor_arr])
        steering = outputs[0]
        throttle = outputs[1]
        return steering[0][0], throttle[0][0]

    def y_transform(self, record: TubRecord):
        angle: float = record.underlying['user/angle']
        throttle: float = record.underlying['user/throttle']
        return angle, throttle

    def y_translate(self, y: XY) -> Dict[str, Union[float, np.ndarray]]:
        if isinstance(y, tuple):
            angle, throttle = y
            return {'n_outputs0': angle, 'n_outputs1': throttle}
        else:
            raise TypeError('Expected tuple')

    def output_shapes(self):
        # pas certain de ce que j'ai fait avec le "sensor_in" ...
    
        # need to cut off None from [None, 120, 160, 3] tensor shape
        img_shape = self.get_input_shape()[1:]
        shapes = ({'img_in': tf.TensorShape(img_shape),
                   'sensor_in': tf.TensorShape([])},
                  {'n_outputs0': tf.TensorShape([]),
                   'n_outputs1': tf.TensorShape([])})
        return shapes

def default_fc_linear(num_outputs, num_sensor_inputs, input_shape=(120, 160, 3)):
    drop = 0.2
    img_in = Input(shape=input_shape, name='img_in')
    x = core_cnn_layers(img_in, drop)
    x = Dense(100, activation='relu', name='dense_1')(x)
    x = Dropout(drop)(x)
    x = Dense(50, activation='relu', name='dense_2')(x)
    x = Dropout(drop)(x)

    sensor_in = Input(shape=(num_sensor_inputs,), name="sensor_in")
    y = sensor_in
    y = Dense(14, activation='relu', name='dense_3')(y)
    y = Dense(14, activation='relu', name='dense_4')(y)
    y = Dense(14, activation='relu', name='dense_5')(y)

    final = concatenate([x, y])
    final = Dense(50, activation='relu', name='dense_6')(final)
    final = Dropout(drop)(final)
    final = Dense(50, activation='relu', name='dense_7')(final)
    final = Dropout(drop)(final)

    outputs = []
    for i in range(num_outputs):
        outputs.append(
            Dense(1, activation='linear', name='n_outputs' + str(i))(final))

    model = Model(inputs=[img_in, sensor_in], outputs=outputs)
    return model
