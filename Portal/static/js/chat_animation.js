// Animation for new chat messages
function animateNewMessage(element) {
    element.style.opacity = 0;
    element.style.transform = 'translateY(20px)';
    setTimeout(() => {
        element.style.transition = 'all 0.4s ease';
        element.style.opacity = 1;
        element.style.transform = 'translateY(0)';
    }, 50);
}
