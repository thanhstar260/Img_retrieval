document.addEventListener("DOMContentLoaded", function () {
    const imageItems = document.querySelectorAll(".image-item");
    const popupContainer = document.querySelector(".popup-container");
    const thumbnailList = document.querySelector(".thumbnail-list");
    let currentImageIndex;
    let currentImageUrl;
    let globalYoutubeLink; // Declare the global variable

    imageItems.forEach((item, index) => {
        item.addEventListener("click", function () {
            currentImageIndex = index;
            const imageUrl = this.querySelector("img").src;
            currentImageUrl = this.querySelector("img").src;
            const altText = this.querySelector("img").alt;
            globalYoutubeLink = parseAltText(altText); // Set the global variable
            const imageName = altText.replace(globalYoutubeLink, "").trim(); // Extract the image name
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
            const index = parseInt(event.target.alt, 10);
            navigateToThumbnail(index);
        }
    });

    function parseAltText(altText) {
        // Use a regular expression to match the YouTube link
        const match = altText.match(/https:\/\/youtu\.be\/[\w-]+(\?.+)?/);

        // Extract the YouTube link
        const youtubeLink = match ? match[0].trim() : null;

        return youtubeLink;
    }

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

        popupContent.appendChild(popupImageName);
        popupContent.appendChild(popupImage);

        const buttonsContainer = document.createElement("div");
        buttonsContainer.className = "buttons";

        // Add search button
        const searchIcon = document.createElement("img");
        searchIcon.src = "/static/icons/search_icon.svg"
        searchIcon.alt = "Search";
        searchIcon.className = "search-icon";
        searchIcon.addEventListener("click", function () {
            // Add your search functionality here
            retrieveImage(currentImageUrl)
        });
        buttonsContainer.appendChild(searchIcon);

        const youtubeIcon = document.createElement("img");
        youtubeIcon.src = "/static/icons/youtube_icon.svg"; // Replace with the actual path to your YouTube icon
        youtubeIcon.alt = "YouTube Icon";
        youtubeIcon.className = "youtube-icon";
        youtubeIcon.addEventListener("click", function () {
            if (globalYoutubeLink) {
                window.open(globalYoutubeLink, '_blank');
            } else {
                alert("No YouTube link available for this image.");
            }
        });
        buttonsContainer.appendChild(youtubeIcon);

        popupContent.appendChild(buttonsContainer);
        popupContainer.innerHTML = "";
        popupContainer.appendChild(popupContent);
        popupContainer.style.display = "flex";

        const thumbnailListContainer = document.createElement("div");
        thumbnailListContainer.className = "thumbnail-list-container";
        popupContent.appendChild(thumbnailListContainer);

        thumbnailListContainer.appendChild(thumbnailList);

        updateThumbnailList();
        document.removeEventListener("keydown", navigateOnKeyPress);
        document.addEventListener("keydown", navigateOnKeyPress);
    }

    function hidePopup() {
        popupContainer.style.display = "none";
        document.removeEventListener("keydown", navigateOnKeyPress);
    }

    function updateThumbnailList() {
        thumbnailList.innerHTML = "";

        for (let i = currentImageIndex - 3; i <= currentImageIndex + 3; i++) {
            const index = (i + imageItems.length) % imageItems.length;
            const thumbnailItem = document.createElement("div");
            thumbnailItem.className = "thumbnail-item";
            const thumbnailImage = document.createElement("img");
            thumbnailImage.src = imageItems[index].querySelector("img").src;
            thumbnailImage.alt = index.toString();
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
        var currentPath = document.querySelector(".popup-image").src;
        var pathArray = currentPath.split('/');
        var filename = pathArray[pathArray.length - 1];
        var directory = pathArray.slice(0, -1).join('/');

        var number = parseInt(filename, 10);
        var nextNumber = number + direction;
        var nextImagePath = getNextImagePath(directory, nextNumber);
        var nextImageName = getNextImageName(directory, nextNumber);

        if (imageExists(nextImagePath)) {
            document.querySelector(".popup-image").src = nextImagePath;
            document.querySelector(".popup-image-name").innerText = nextImageName;
            currentImageIndex = (currentImageIndex + direction + imageItems.length) % imageItems.length;
            updateThumbnailList();
        }
    }

    function navigateToThumbnail(index) {
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
        return name.slice(36);
    } 

    function retrieveImage(query) {
        let route;
        route = '/retrieve_image';
    
        fetch(route, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                image_query: query,
                k_value: 80,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Server response:', data);
            if (data.result) {
                // Create a new container to hold the updated results
                const newResultsContainer = document.createElement('div');
                newResultsContainer.className = 'container';
    
                const imageContainer = document.createElement('div');
                imageContainer.className = 'image-container';
    
                data.result.forEach(item => {
                    const imageItem = document.createElement('div');
                    imageItem.className = 'image-item';
                    const image = document.createElement('img');
                    image.src = item[0];
                    image.alt = item[0].slice(15) + item[1];
                    imageItem.appendChild(image);
                    imageContainer.appendChild(imageItem);
                });
    
                newResultsContainer.appendChild(imageContainer);

                // Replace the existing container with the new one
                const existingResultsContainer = document.querySelector('.container');
                existingResultsContainer.replaceWith(newResultsContainer);

                const Container = document.querySelector('.container');
                Container.style.marginLeft = '2rem';
    
                // Reattach the event listeners to the new images
                attachEventListeners();
    
                // Close the popup
                hidePopup();
            }
        })
        .catch(error => {
            console.error('Error during AJAX request:', error);
        });
    }
    
    function attachEventListeners() {
        const imageItems = document.querySelectorAll(".image-item");
        
        imageItems.forEach((item, index) => {
            item.addEventListener("click", function () {
                currentImageIndex = index;
                const imageUrl = this.querySelector("img").src;
                currentImageUrl = this.querySelector("img").src;
                const altText = this.querySelector("img").alt;
                globalYoutubeLink = parseAltText(altText); // Set the global variable
                const imageName = altText.replace(globalYoutubeLink, "").trim(); // Extract the image name
                showPopup(imageUrl, imageName);
            });
        });
    }
    
});
