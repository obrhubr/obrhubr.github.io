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
    TARGET_WIDTHS = [1080, 720, 640, 480, 320]

    def resize_images(content)
      @resized_images_to_cleanup ||= []
      doc = Nokogiri::HTML.fragment(content)
      doc.css('img').each do |img|
        src = img['src']
        next unless src

        resized_images = resize_image(src)

        # Set the srcset attribute
        img['srcset'] = build_srcset(resized_images)

        # Get the largest image (1080px) dimensions
        largest_image_path = File.join(@context.registers[:site].source, resized_images[1080])
        if File.exist?(largest_image_path)
          largest_image = MiniMagick::Image.open(largest_image_path)
          img['width'] = largest_image.width
          img['height'] = largest_image.height
        end

        # Store resized images for later cleanup
        @resized_images_to_cleanup.concat(resized_images.values)
      end
      doc.to_html
    end

    def resize_image(src)
      site = @context.registers[:site]
      source_dir = site.source
      image = MiniMagick::Image.open(File.join(source_dir, src))
      resized_images = {}

      TARGET_WIDTHS.each do |width|
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

    def build_srcset(resized_images)
      resized_images.map { |width, file| "#{file} #{width}w" }.join(', ')
    end
  end
end

Liquid::Template.register_filter(Jekyll::ImageResizer)
