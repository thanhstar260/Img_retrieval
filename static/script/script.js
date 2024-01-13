document.addEventListener("DOMContentLoaded", function () {
    const imageItems = document.querySelectorAll(".image-item");
    const popupContainer = document.querySelector(".popup-container");
    let currentImageIndex = 0;
    let images = [];

    imageItems.forEach((item, index) => {
        const imageUrl = item.querySelector("img").src;
        const imageName = item.querySelector("img").alt;
        images.push({ src: imageUrl, alt: imageName, index });
        item.addEventListener("click", function () {
            currentImageIndex = index;
            showPopup();
        });
    });

    popupContainer.addEventListener("click", function () {
        hidePopup();
    });

    function showPopup() {
        const popupContent = document.createElement("div");
        popupContent.className = "popup-content";

        const popupImageName = document.createElement("p");
        popupImageName.innerText = images[currentImageIndex].alt;
        popupImageName.className = "popup-image-name";

        const popupImage = document.createElement("img");
        popupImage.src = images[currentImageIndex].src;
        popupImage.alt = images[currentImageIndex].alt;
        popupImage.className = "popup-image";

        popupContent.appendChild(popupImageName);
        popupContent.appendChild(popupImage);
        popupContainer.innerHTML = "";
        popupContainer.appendChild(popupContent);

        popupContainer.style.display = "flex";
    }

    function hidePopup() {
        popupContainer.style.display = "none";
    }

    document.addEventListener("keydown", function (event) {
        if (popupContainer.style.display === "flex") {
            if (event.key === "ArrowLeft") {
                currentImageIndex = (currentImageIndex - 1 + images.length) % images.length;
                showPopup();
            } else if (event.key === "ArrowRight") {
                currentImageIndex = (currentImageIndex + 1) % images.length;
                showPopup();
            }
        }
    });
});
