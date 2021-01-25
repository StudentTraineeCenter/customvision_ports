# customvision_ports

Web app using model trained in Custom Vision that detects and classifies several types of ports. 

Custom Vision is one of Microsoft's Azure Cognitive Services. We used it to train object detection model which draws bounding boxes around USB-C, Micro-USB, USB-B and Lightning male ports. You can view the website here: https://portvision.azurewebsites.net/ or you can look at our article with further details: https://studuj.digital/category/azure/.

We use python framework Flask for backend and integration of trained model exported from the service.
