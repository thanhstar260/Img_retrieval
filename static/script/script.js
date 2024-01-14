document.addEventListener("DOMContentLoaded", function () {
    const imageItems = document.querySelectorAll(".image-item");
    const popupContainer = document.querySelector(".popup-container");
    let currentImageIndex;

    imageItems.forEach((item, index) => {
        item.addEventListener("click", function () {
            currentImageIndex = index;
            const imageUrl = this.querySelector("img").src;
            const imageName = this.querySelector("img").alt;
            showPopup(imageUrl, imageName);
        });
    });

    popupContainer.addEventListener("click", function (event) {
        if (event.target === popupContainer) {
            hidePopup();
        }
    });

    function showPopup(imageUrl, imageName) {
        const popupContent = document.createElement("div");
        popupContent.className = "popup-content";

        const popupImageName = document.createElement("p");
        popupImageName.innerText = imageName;
        popupImageName.className = "popup-image-name";

        const popupImage = document.createElement("img");
        popupImage.src = imageUrl;
        popupImage.alt = imageName;  // Set alt attribute to the image name
        popupImage.className = "popup-image";

        popupContent.appendChild(popupImageName);
        popupContent.appendChild(popupImage);
        popupContainer.innerHTML = ""; // This line may not be necessary
        popupContainer.appendChild(popupContent);

        popupContainer.style.display = "flex";

        // Remove existing event listener before adding a new one
        document.removeEventListener("keydown", navigateOnKeyPress);

        // Add event listener for arrow key navigation
        document.addEventListener("keydown", navigateOnKeyPress);
    }

    function hidePopup() {
        popupContainer.style.display = "none";

        // Remove event listener for arrow key navigation
        document.removeEventListener("keydown", navigateOnKeyPress);
    }

    function navigateOnKeyPress(event) {
        if (popupContainer.style.display === "flex") {
            if (event.key === "ArrowLeft") {
                navigate(-1);
            } else if (event.key === "ArrowRight") {
                navigate(1);
            }
        }
    }

    function navigate(direction) {
        // Extract the filename and path from the current image source
        var currentPath = document.querySelector(".popup-image").src;
        var pathArray = currentPath.split('/');
        var filename = pathArray[pathArray.length - 1];
        var directory = pathArray.slice(0, -1).join('/');

        // Extract the number from the filename
        var number = parseInt(filename, 10);

        // Update the image source based on the navigation direction
        var nextNumber = number + direction;
        var nextImagePath = getNextImagePath(directory, nextNumber);
        var nextImageName = getNextImageName(directory, nextNumber);

        // Check if the next image exists
        if (!imageExists(nextImagePath)) {
            // If the next image doesn't exist, do nothing and return
            console.warn("Next image does not exist. Keeping the current image.");
            return;
        }

        // Update the popup with the next image
        document.querySelector(".popup-image").src = nextImagePath;
        document.querySelector(".popup-image-name").innerText = nextImageName;
    }

    function getNextImagePath(directory, nextNumber) {
        if (nextNumber < 10) {
            return directory + '/000' + nextNumber + '.jpg';
        } else if (nextNumber < 100) {
            return directory + '/00' + nextNumber + '.jpg';
        } else {
            return directory + '/0' + nextNumber + '.jpg';
        }
    }

    function getNextImageName(directory, nextNumber) {
        var name = getNextImagePath(directory, nextNumber);
        return name.slice(36)
    }

    // Function to check if an image exists
    function imageExists(imagePath) {
        var http = new XMLHttpRequest();
        http.open('HEAD', imagePath, false);
        http.send();
        return http.status !== 404;
    }
});
