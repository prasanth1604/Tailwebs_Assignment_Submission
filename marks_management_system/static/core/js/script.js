document.addEventListener('DOMContentLoaded', function() {
    // Select all message list items
    const messages = document.querySelectorAll('.messages li');

    if (messages.length > 0) {
        messages.forEach(message => {
            // Set a timeout to fade out the message
            setTimeout(() => {
                message.classList.add('fade-out');
                // Remove the message from the DOM after the fade-out transition
                message.addEventListener('transitionend', () => {
                    message.remove();
                });
            }, 5000); // 5000 milliseconds = 5 seconds
        });
    }
});