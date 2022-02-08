#F&C Openvino API part
import os
import numpy as np
import cv2
from typing import Union, Tuple
from openvino.inference_engine import IECore, Blob, TensorDesc

ONE_BYTE_SCALE = 1.0 / 255.0

class FC_Openvino:
    def __init__(self, device_type, model_path):
        openvino_xml = os.path.splitext(model_path)[0] +".xml"
        openvino_bin = os.path.splitext(model_path)[0] +".bin"
        print("F&C : Loading Openvino model using " + device_type + " device type...")
        ie_core_handler = IECore()
        print("F&C : Available Openvino devices : " + str(ie_core_handler.available_devices))
        
        network = ie_core_handler.read_network(model=openvino_xml, weights=openvino_bin)
        self.exec_net = ie_core_handler.load_network(network, device_name=device_type, num_requests=1)
        self.inference_request = self.exec_net.requests[0]
        
        input_blobs = self.inference_request.input_blobs
        output_blobs = self.inference_request.output_blobs
        self.input_blob_name = next(iter(input_blobs))
        iterList = iter(output_blobs)
        self.output_blob_name0 = next(iterList) #Steering
        self.output_blob_name1 = next(iterList) #Throttle

        print("F&C : Model loaded.")

        
    def run(self, img_arr: np.ndarray, other_arr: np.ndarray = None) \
            -> Tuple[Union[float, np.ndarray], ...]:
            
            imageHeight, imageWidth, imageColorLayers = img_arr.shape
            
            img_arr = img_arr.astype(np.float64) * ONE_BYTE_SCALE
            img_arr = np.float32(img_arr.reshape(1, imageHeight, imageWidth, imageColorLayers)) #NHWC
            
            tensor_description = TensorDesc(precision="FP32", dims=(1, imageColorLayers, imageHeight, imageWidth), layout='NCHW')
            input_blob = Blob(tensor_description, img_arr)
            
            self.inference_request.set_blob(blob_name=self.input_blob_name, blob=input_blob)
            self.inference_request.infer()

            output_blobs = self.inference_request.output_blobs
            steering = output_blobs[self.output_blob_name0].buffer
            throttle = output_blobs[self.output_blob_name1].buffer
            return float(steering[0][0]), float(throttle[0][0])