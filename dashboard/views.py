from django.shortcuts import render
from django.http import HttpResponse
from matplotlib import pyplot as plt
from skimage import data
from skimage.feature import blob_dog, blob_log, blob_doh
from math import sqrt
from skimage.color import rgb2gray
import glob
from skimage.io import imread
from django.core.files.storage import default_storage
from matplotlib.backends.backend_agg import FigureCanvas
from io import BytesIO
import base64

def dashboard(request):

	if request.method == "POST":
		# print(request.FILES['sentFile'])
		f = request.FILES['image'] # here you get the files needed
		response = {}
		file_name = "pic.jpg"
		file_name_2 = default_storage.save(file_name, f)
		file_url = default_storage.url(file_name_2)
		original = glob.glob(file_url)
		numpy_image = imread(original[0], as_grey=True)
		# plt.imshow(numpy_image, cmap=cm.gray)
		# plt.show()

		print('hey')
		blobs_log = blob_log(numpy_image, max_sigma=30, num_sigma=10, threshold=.1)
		# Compute radii in the 3rd column.
		blobs_log[:, 2] = blobs_log[:, 2] * sqrt(2)
		numrows = len(blobs_log)
		print("Number of stars counted : " ,numrows)
		response['n_stars'] = str(numrows)

		fig, ax = plt.subplots(1, 1)
		plt.imshow(numpy_image)
		for blob in blobs_log:
			y, x, r = blob
			c = plt.Circle((x, y), r+5, color='lime', linewidth=2, fill=False)
			ax.add_patch(c)
		# response['image'] = HttpResponse(content_type='image/jpg')
		# FigureCanvas(fig).print_jpeg(response['image'])
		buffer = BytesIO()
		plt.savefig(buffer, format='png')
		buffer.seek(0)
		image_png = buffer.getvalue()
		buffer.close()

		graphic = base64.b64encode(image_png)
		graphic = graphic.decode('utf-8')
		response['image'] = graphic

		return render(request,'calculation.html',response)
	else:
		return render(request,'homepage.html')
