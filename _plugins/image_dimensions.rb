require 'nokogiri'
require 'fastimage'
require 'pathname'

module Jekyll
	module ImageSizeFilter
		def add_image_size(content)
			# Parse the HTML content using Nokogiri
			doc = Nokogiri::HTML(content)

			# Base directory where the images are located
			base_dir = Jekyll.configuration({})['source']

			# Iterate over each image tag in the content
			doc.css('img').each do |img|
				# Skip if the image already has width and height attributes
				next if img['width'] && img['height']

					# Get the image source URL
					img_src = img['src']

					# Construct the full file path
					img_path = File.join(base_dir, img_src)

					# Check if the file exists
					if File.exist?(img_path)
						# Use FastImage to determine the dimensions of the image
						size = FastImage.size(img_path)
						if size
							img['width'] = size[0].to_s unless img['width']
							img['height'] = size[1].to_s unless img['height']
						end
					end
				end

			# Return the modified HTML
			doc.to_html
		end
	end
end

Liquid::Template.register_filter(Jekyll::ImageSizeFilter)