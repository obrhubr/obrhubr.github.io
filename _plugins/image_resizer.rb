require 'mini_magick'
require 'nokogiri'
require 'fileutils'

module Jekyll
	class ResizedImage < StaticFile
		def initialize(site, base, dir, name, dest_dir)
			super(site, base, dir, name)
			@dest_dir = dest_dir
		end

		def destination(dest)
			File.join(dest, @dest_dir, @name)
		end

		def write(dest)
			super(dest)
		end
	end

	module ImageResizer
		TARGET_WIDTHS = [800, 720, 640, 480, 320]

		def resize_images(content)
			# Only resize images in production build
			if ENV['JEKYLL_ENV'] == "production"
				# Get HTML nodes from content
				doc = Nokogiri::HTML.fragment(content)

				# Iterate through all images
				doc.css('img').each do |img|
					# Get src of image
					src = img['src']
					next unless src

					# Check if the file is a GIF
					if File.extname(src).downcase == '.gif'
						next # Skip resizing for GIFs
					end

					# Check if image should be kept in original form
					if src.include?(".keep.")
						next
					end

					# Resize the image and include the original in the srcset
					resized_images = resize_image(src)

					# Set the srcset attribute
					img['srcset'] = build_srcset(src, resized_images)
					# Set the sizes attribute
					img['sizes'] = "(max-width: 800px) 100vw, (min-width: 801px) 800px"

					# Set the src attribute to the original image
					img['src'] = src

					# Get the default dimensions from the original image
					original_image_path = File.join(@context.registers[:site].source, src)
					if File.exist?(original_image_path)
						original_image = MiniMagick::Image.open(original_image_path)
						img['width'] = original_image.width
						img['height'] = original_image.height
					end
				end
				doc.to_html
			else
				content
			end
		end

		def resize_image(src)
			site = @context.registers[:site]
			
			source_dir = site.source
			image = MiniMagick::Image.open(File.join(source_dir, src))
			resized_images = {}

			TARGET_WIDTHS.each do |width|
				if image.width > width
					output_file_name = "#{File.basename(src, '.*')}-#{width}.#{image.type.downcase}"
					output_file_path = File.join(File.dirname(src), output_file_name)

					# Ensure the directory exists before attempting to write the file
					output_dir = File.join(source_dir, File.dirname(src))
					FileUtils.mkdir_p(output_dir) unless Dir.exist?(output_dir)

					# Resize and write the image
					unless resized_images.values.include?(output_file_path)
						resized_image_path = generate_resized_image(image, output_file_name, width, output_dir)
						resized_images[width] = output_file_path if resized_image_path

						# Add the file to the static files to ensure Jekyll copies it
						site.static_files << Jekyll::ResizedImage.new(site, source_dir, File.dirname(src), output_file_name, File.dirname(src))
					end
				end
			end

			resized_images
		end

		def generate_resized_image(image, output_file_name, width, output_dir)
			output_path = File.join(output_dir, output_file_name)

			unless File.exist?(output_path)
				resized_image = image.clone
				resized_image.resize "#{width}x"
				resized_image.write(output_path)
			end

			output_file_name
		end

		def build_srcset(original_src, resized_images)
			srcset = resized_images.map { |width, file| "#{file} #{width}w" }.join(', ')
			# Add the original image as the default (highest resolution) version
			"#{original_src} #{MiniMagick::Image.open(File.join(@context.registers[:site].source, original_src)).width}w, " + srcset
		end
	end
end

Liquid::Template.register_filter(Jekyll::ImageResizer)
