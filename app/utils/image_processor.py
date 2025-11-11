import os
from werkzeug.utils import secure_filename
from PIL import Image
from flask import current_app


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']


def convert_to_webp(image_path, output_path=None, quality=85):
    """
    Convert image to WebP format
    
    Args:
        image_path: Path to the source image
        output_path: Path for the output WebP file (optional)
        quality: WebP quality (0-100), default 85
    
    Returns:
        Path to the converted WebP file
    """
    try:
        # Open the image
        img = Image.open(image_path)
        
        # Convert RGBA to RGB if necessary (WebP supports RGBA, but we'll use RGB for compatibility)
        if img.mode == 'RGBA':
            # Create a white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            img = background
        elif img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        
        # Generate output path if not provided
        if output_path is None:
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(
                os.path.dirname(image_path),
                f"{base_name}.webp"
            )
        
        # Save as WebP
        img.save(output_path, 'WEBP', quality=quality, optimize=True)
        
        # Remove original file
        if os.path.exists(image_path) and image_path != output_path:
            os.remove(image_path)
        
        return output_path
    except Exception as e:
        raise Exception(f"Error converting image to WebP: {str(e)}")


def save_uploaded_image(file, subfolder=''):
    """
    Save uploaded image and convert to WebP
    
    Args:
        file: Flask file object
        subfolder: Optional subfolder within uploads directory
    
    Returns:
        Path to the saved WebP file (relative to uploads folder)
    """
    if file and allowed_file(file.filename):
        # Secure the filename
        filename = secure_filename(file.filename)
        
        # Create subfolder if specified
        upload_folder = current_app.config['UPLOAD_FOLDER']
        if subfolder:
            upload_folder = os.path.join(upload_folder, subfolder)
            os.makedirs(upload_folder, exist_ok=True)
        
        # Generate unique filename to avoid conflicts
        from datetime import datetime
        import uuid
        base_name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        unique_filename = f"{base_name}_{uuid.uuid4().hex[:8]}{extension}"
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Save the file
        file.save(file_path)
        
        # Convert to WebP
        webp_path = convert_to_webp(file_path)
        
        # Return relative path from uploads folder
        relative_path = os.path.relpath(webp_path, current_app.config['UPLOAD_FOLDER'])
        return relative_path.replace('\\', '/')  # Normalize path separators
    
    raise ValueError("Invalid file type or no file provided")

