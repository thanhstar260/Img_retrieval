document.addEventListener("DOMContentLoaded", function () {
    const imageItems = document.querySelectorAll(".image-item");
    const popupContainer = document.querySelector(".popup-container");
    const thumbnailList = document.querySelector(".thumbnail-list");
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

    thumbnailList.addEventListener("click", function (event) {
        if (event.target.tagName === "IMG") {
            // Extract the index from the thumbnail's alt attribute
            const index = parseInt(event.target.alt, 10);
            navigateToThumbnail(index);
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
        popupImage.alt = imageName;
        popupImage.className = "popup-image";
    
        const thumbnailListContainer = document.createElement("div");
        thumbnailListContainer.className = "thumbnail-list-container";
    
        popupContent.appendChild(popupImageName);
        popupContent.appendChild(popupImage);
        popupContent.appendChild(thumbnailListContainer); // Append the thumbnail list container
    
        popupContainer.innerHTML = "";
        popupContainer.appendChild(popupContent);
    
        popupContainer.style.display = "flex";
    
        // Append the thumbnail list to the container
        thumbnailListContainer.appendChild(thumbnailList);
    
        updateThumbnailList();
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

    function updateThumbnailList() {
        // Clear existing thumbnails
        thumbnailList.innerHTML = "";

        // Display thumbnails for a larger range around the current image
        for (let i = currentImageIndex - 3; i <= currentImageIndex + 3; i++) {
            const index = (i + imageItems.length) % imageItems.length; // Ensure circular indexing
            const thumbnailItem = document.createElement("div");
            thumbnailItem.className = "thumbnail-item";
            const thumbnailImage = document.createElement("img");
            thumbnailImage.src = imageItems[index].querySelector("img").src;
            thumbnailImage.alt = index.toString();  // Set alt attribute to the index
            thumbnailItem.appendChild(thumbnailImage);
            thumbnailList.appendChild(thumbnailItem);
        }
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
        if (imageExists(nextImagePath)) {
            document.querySelector(".popup-image").src = nextImagePath;
            document.querySelector(".popup-image-name").innerText = nextImageName;
            currentImageIndex = (currentImageIndex + direction + imageItems.length) % imageItems.length; // Ensure circular indexing
            updateThumbnailList();
        }
    }

    function navigateToThumbnail(index) {
        // Navigate to the selected thumbnail image
        const thumbnailImagePath = imageItems[index].querySelector("img").src;
        const thumbnailImageName = imageItems[index].querySelector("img").alt;

        document.querySelector(".popup-image").src = thumbnailImagePath;
        document.querySelector(".popup-image-name").innerText = thumbnailImageName;
        currentImageIndex = index;
        updateThumbnailList();
    }

    function imageExists(imagePath) {
        const http = new XMLHttpRequest();
        http.open('HEAD', imagePath, false);
        http.send();
        return http.status !== 404;
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
});
