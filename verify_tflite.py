import cv2
import numpy as np
import tensorflow as tf

# Load the TFLite model
tflite_model_path = 'best-fp16.tflite'
interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height, width = input_details[0]['shape'][1:3]

# Load an example image for inference
image_path = 'manikin2.jpg'
image = cv2.imread(image_path)
print("width, height", width, height)
image = cv2.resize(image, (width, height))
image = image / 255.0  # Normalize to [0, 1]
image = np.expand_dims(image, axis=0)

# Set input tensor
interpreter.set_tensor(input_details[0]['index'], image.astype(np.float32))

# Run inference
interpreter.invoke()

# Get the output tensor
output_data = interpreter.get_tensor(output_details[0]['index'])

# Post-process the output (adjust based on the structure of your YOLOv5 output)
# For example, you might extract bounding box coordinates and class scores
# and apply non-maximum suppression to get the final detections.

# Display the results (adjust based on your post-processing)
for detection in output_data[0]:
    confidence = detection[4]

    if confidence > 0.5:  # Filter out low-confidence detections
        print('detection', detection)
        xmin, ymin, xmax, ymax = (detection[:4] * [width, height, width, height]).astype(int)
        class_id = int(detection[5])

        # Draw bounding box and label on the image
        cv2.rectangle(image[0], (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        cv2.putText(image[0], f'Class {class_id} ({confidence:.2f})', (xmin, ymin - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the image with detections
cv2.imshow('Inference Result', image[0])
cv2.waitKey(0)
cv2.destroyAllWindows()