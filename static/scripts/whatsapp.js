document.getElementById('whatsappBtn').addEventListener('click', function() {
    var phoneNumber = '+971547915699';
    var message = "Hello, I'm interested to know about 800doctor services. Please let me know.";
    var whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;

    window.open(whatsappUrl, '_blank');
});