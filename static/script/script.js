document.addEventListener("DOMContentLoaded", function () {
    const imageItems = document.querySelectorAll(".image-item");
    const popupContainer = document.querySelector(".popup-container");
    const thumbnailList = document.querySelector(".thumbnail-list");
    let currentImageIndex;
    let currentImageUrl;
    let youtubeLinks;

    imageItems.forEach((item, index) => {
        item.addEventListener("click", function () {
            currentImageIndex = index;
            const imageUrl = this.querySelector("img").src;
            currentImageUrl = imageUrl; // Update currentImageUrl when an image is clicked
            const imageName = this.querySelector("img").alt;;
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

    fetch('./static/path2link.json')
    .then(response => response.json())
    .then(data => {
        console.log(data)
        console.log(Object.keys(data).length);
        youtubeLinks = data;
    })
    .catch(error => {
        console.error('Error loading the JSON file:', error);
    });

    function showPopup(imageUrl, imageName) {
        currentImageUrl = imageUrl; // Update currentImageUrl when showing the popup
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

        const searchIcon = document.createElement("img");
        searchIcon.src = "/static/icons/search_icon.svg"
        searchIcon.alt = "Search";
        searchIcon.className = "search-icon";
        searchIcon.addEventListener("click", function () {
            retrieveImage(currentImageUrl); // Use currentImageUrl for search
        });
        buttonsContainer.appendChild(searchIcon);

        const youtubeIcon = document.createElement("img");
        youtubeIcon.src = "/static/icons/youtube_icon.svg";
        youtubeIcon.alt = "YouTube Icon";
        youtubeIcon.className = "youtube-icon";
        youtubeIcon.addEventListener("click", function () {
            handleYoutubeIconClick()
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

        const currentNumber = parseInt(currentImageUrl.split('/').pop().split('.')[0], 10);
        const directory = currentImageUrl.substring(0, currentImageUrl.lastIndexOf("/"));

        const maxIndex = currentNumber + 3;
        const minIndex = Math.max(1, currentNumber - 3);

        for (let i = minIndex; i <= maxIndex; i++) {
            const paddedNumber = String(i).padStart(4, '0');
            const imagePath = `${directory}/${paddedNumber}.jpg`;
            if (imageExists(imagePath)) {
                const thumbnailItem = document.createElement("div");
                thumbnailItem.className = "thumbnail-item";
                if (i === currentNumber) {
                    thumbnailItem.classList.add("current-thumbnail"); // Add class to highlight current image
                }
                const thumbnailImage = document.createElement("img");
                thumbnailImage.src = imagePath;
                thumbnailImage.alt = getImageName(directory, paddedNumber); // Set alt to the correct format
                thumbnailImage.addEventListener("click", function(event) {
                    showPopup(event.target.src, event.target.alt); // Show the clicked image in the popup
                });
                thumbnailItem.appendChild(thumbnailImage);
                thumbnailList.appendChild(thumbnailItem);
            }
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
        var nextImageName = getImageName(directory, nextNumber);
    
        if (imageExists(nextImagePath)) {
            currentImageIndex = (currentImageIndex + direction + imageItems.length) % imageItems.length;
    
            currentImageUrl = nextImagePath; // Update currentImageUrl when navigating
    
            const popupImage = document.querySelector(".popup-image");
            popupImage.src = currentImageUrl;
            popupImage.alt = nextImageName;
            document.querySelector(".popup-image-name").innerText = nextImageName;
    
            const buttonsContainer = document.querySelector(".buttons");
            const youtubeIcon = buttonsContainer.querySelector(".youtube-icon");
            youtubeIcon.removeEventListener("click", handleYoutubeIconClick);
            youtubeIcon.addEventListener("click", handleYoutubeIconClick);
    
            updateThumbnailList(); // Update thumbnail list after navigating
        }
    }          

    function navigateToThumbnail(index) {
        const thumbnailImagePath = imageItems[index].querySelector("img").src;
        const thumbnailImageName = imageItems[index].querySelector("img").alt;

        currentImageUrl = thumbnailImagePath; // Update currentImageUrl when navigating to a thumbnail
        document.querySelector(".popup-image").src = thumbnailImagePath;
        document.querySelector(".popup-image-name").innerText = thumbnailImageName;
        currentImageIndex = index;
        updateThumbnailList();
    }

    function handleYoutubeIconClick() {
        const currentImageName = document.querySelector(".popup-image").alt;
        console.log(currentImageName)
        // Check if youtubeLinks is loaded
        if (youtubeLinks) {
            const youtubeLink = youtubeLinks[currentImageName];
            if (youtubeLink) {
                window.open(youtubeLink, '_blank');
            } else {
                console.error("YouTube link not found for the current image.");
            }
        } else {
            console.error("YouTube links not loaded yet.");
        }
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

    function getImageName(directory, paddedNumber) {
        const parts = directory.split('/');
        // console.log(parts)
        const sequenceName = parts[parts.length - 2];
        const versionNumber = parts[parts.length - 1];
        const number = String(paddedNumber).padStart(4, '0');
        return `${sequenceName}/${versionNumber}/${number}.jpg`;
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
                const newResultsContainer = document.createElement('div');
                newResultsContainer.className = 'container';
    
                let imageContainer = document.createElement('div'); // Declare imageContainer here
                imageContainer.className = 'image-container';
    
                let i = 1;
    
                data.result.forEach(item => {
                    const imageItem = document.createElement('div');
                    imageItem.className = 'image-item';
                    const image = document.createElement('img');
                    image.src = item;
                    image.alt = item.slice(16);
                    imageItem.appendChild(image);
                    imageContainer.appendChild(imageItem);
                    if (i % 6 == 0) {
                        newResultsContainer.appendChild(imageContainer);
                        imageContainer = document.createElement('div'); // Update imageContainer's contents
                        imageContainer.className = 'image-container';
                    }
                    i++;
                });
    
                // Append any remaining images
                if (imageContainer.children.length > 0) {
                    newResultsContainer.appendChild(imageContainer);
                }
    
                const existingResultsContainer = document.querySelector('.container');
                existingResultsContainer.replaceWith(newResultsContainer);
                attachEventListeners();
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
                currentImageUrl = imageUrl; // Update currentImageUrl when an image is clicked 
                const imageName = this.querySelector("img").alt;
                console.log(imageName)
                showPopup(imageUrl, imageName);
            });
        });
    }
});
