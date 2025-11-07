// Gallery functionality
let currentImageIndex = 0;
let images = [];

// Initialize gallery
document.addEventListener('DOMContentLoaded', () => {
    const thumbnails = document.querySelectorAll('.gallery-thumbnails img');
    images = Array.from(thumbnails).map(img => img.src);
    
    if (thumbnails.length > 0) {
        currentImageIndex = 0;
    }
});

// Change main image
function setMainImage(imageSrc) {
    const mainImage = document.getElementById('mainImage');
    mainImage.style.opacity = '0';
    
    setTimeout(() => {
        mainImage.src = imageSrc;
        mainImage.style.opacity = '1';
    }, 200);
    
    // Update active thumbnail
    document.querySelectorAll('.gallery-thumbnails img').forEach((img, index) => {
        img.classList.remove('active');
        if (img.src === imageSrc) {
            img.classList.add('active');
            currentImageIndex = index;
        }
    });
}

// Navigate gallery
function changeImage(direction) {
    currentImageIndex += direction;
    
    if (currentImageIndex < 0) {
        currentImageIndex = images.length - 1;
    } else if (currentImageIndex >= images.length) {
        currentImageIndex = 0;
    }
    
    setMainImage(images[currentImageIndex]);
}

// Lightbox functionality
function openLightbox() {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightboxImg');
    const mainImage = document.getElementById('mainImage');
    
    lightbox.classList.add('active');
    lightboxImg.src = mainImage.src;
    document.body.style.overflow = 'hidden';
}

function closeLightbox() {
    const lightbox = document.getElementById('lightbox');
    lightbox.classList.remove('active');
    document.body.style.overflow = 'auto';
}

function lightboxNav(direction) {
    changeImage(direction);
    const lightboxImg = document.getElementById('lightboxImg');
    lightboxImg.style.opacity = '0';
    
    setTimeout(() => {
        lightboxImg.src = images[currentImageIndex];
        lightboxImg.style.opacity = '1';
    }, 200);
}

// Close lightbox on escape key
document.addEventListener('keydown', (e) => {
    const lightbox = document.getElementById('lightbox');
    if (e.key === 'Escape' && lightbox.classList.contains('active')) {
        closeLightbox();
    } else if (lightbox.classList.contains('active')) {
        if (e.key === 'ArrowLeft') {
            lightboxNav(-1);
        } else if (e.key === 'ArrowRight') {
            lightboxNav(1);
        }
    }
});

// Close lightbox on click outside
document.getElementById('lightbox')?.addEventListener('click', (e) => {
    if (e.target.id === 'lightbox') {
        closeLightbox();
    }
});

// Keyboard navigation for gallery
document.addEventListener('keydown', (e) => {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox || !lightbox.classList.contains('active')) {
        if (e.key === 'ArrowLeft') {
            changeImage(-1);
        } else if (e.key === 'ArrowRight') {
            changeImage(1);
        }
    }
});

// Touch swipe for mobile
let touchStartX = 0;
let touchEndX = 0;

const galleryMain = document.querySelector('.gallery-main');

galleryMain?.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

galleryMain?.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
});

function handleSwipe() {
    if (touchEndX < touchStartX - 50) {
        changeImage(1);
    }
    if (touchEndX > touchStartX + 50) {
        changeImage(-1);
    }
}

// Auto-play gallery (optional)
let autoplayInterval;

function startAutoplay() {
    autoplayInterval = setInterval(() => {
        changeImage(1);
    }, 5000);
}

function stopAutoplay() {
    clearInterval(autoplayInterval);
}

// Uncomment to enable autoplay
// startAutoplay();

// Stop autoplay on user interaction
galleryMain?.addEventListener('mouseenter', stopAutoplay);
galleryMain?.addEventListener('mouseleave', startAutoplay);