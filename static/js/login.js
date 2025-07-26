// Background Slideshow
let currentBg = 0;
const bgImages = document.querySelectorAll('.bg-img');

function changeBackground() {
    bgImages[currentBg].classList.remove('active');
    currentBg = (currentBg + 1) % bgImages.length;
    bgImages[currentBg].classList.add('active');
}
setInterval(changeBackground, 7000);

// Login Form Handling
const loginForm = document.getElementById('loginForm');
const errorMsg = document.getElementById('errorMsg');
const lockMsg = document.getElementById('lockMsg');

let failedAttempts = 0;
let lockUntil = 0;
let lockTimer = null;

loginForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const pharmacyCode = document.getElementById('pharmacyCode').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // Client-side validation
    if (!pharmacyCode || !username || !password) {
        errorMsg.textContent = 'All fields are required';
        loginForm.classList.add('animate__animated', 'animate__headShake');
        setTimeout(() => {
            loginForm.classList.remove('animate__animated', 'animate__headShake');
        }, 1000);
        return;
    }
    
    // Check if account is locked (client-side)
    const now = Date.now();
    if (now < lockUntil) {
        const remainingTime = Math.ceil((lockUntil - now) / 1000);
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;
        lockMsg.textContent = `Account locked. Try again in ${minutes}m ${seconds}s`;
        errorMsg.textContent = '';
        return;
    }
    
    // Submit to server
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'pharmacyCode': pharmacyCode,
            'username': username,
            'password': password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = "/dashboard";
        } else {
            // Handle failed login
            failedAttempts++;
            
            if (data.locked) {
                lockUntil = now + 300000; // 5 minutes lock
                lockMsg.textContent = "Too many failed attempts. Try again after 5 minutes.";
                
                // Start lock timer
                if (lockTimer) clearInterval(lockTimer);
                lockTimer = setInterval(updateLockMessage, 1000);
            } else {
                errorMsg.textContent = data.message || `Invalid credentials. Attempts left: ${3 - failedAttempts}`;
                lockMsg.textContent = '';
            }
            
            // Clear form and shake animation
            loginForm.reset();
            loginForm.classList.add('animate__animated', 'animate__headShake');
            setTimeout(() => {
                loginForm.classList.remove('animate__animated', 'animate__headShake');
            }, 1000);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        errorMsg.textContent = 'An error occurred during login';
    });
});

function updateLockMessage() {
    const now = Date.now();
    if (now >= lockUntil) {
        clearInterval(lockTimer);
        lockMsg.textContent = '';
        failedAttempts = 0;
    } else {
        const remainingTime = Math.ceil((lockUntil - now) / 1000);
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;
        lockMsg.textContent = `Account locked. Try again in ${minutes}m ${seconds}s`;
    }
}

// 3D Input Focus Effect
const inputs = document.querySelectorAll('.form-group input');

inputs.forEach(input => {
    input.addEventListener('focus', () => {
        input.parentNode.style.transform = 'translateZ(20px)';
    });
    
    input.addEventListener('blur', () => {
        input.parentNode.style.transform = 'translateZ(0)';
    });
});

// Display flash messages if they exist
document.addEventListener('DOMContentLoaded', function() {
    const flashError = "{{ get_flashed_messages(category_filter=['error'])[0] if get_flashed_messages(category_filter=['error']) else '' }}";
    if (flashError) {
        errorMsg.textContent = flashError;
        loginForm.classList.add('animate__animated', 'animate__headShake');
        setTimeout(() => {
            loginForm.classList.remove('animate__animated', 'animate__headShake');
        }, 1000);
    }
});