document.addEventListener("DOMContentLoaded", function () {
    const imageItems = document.querySelectorAll(".image-item");
    const popupContainer = document.querySelector(".popup-container");
    let currentImageIndex;
    let currentImageUrl;
    let globalYoutubeLink;
    let thumbnailList; // Define thumbnailList here

    imageItems.forEach((item, index) => {
        item.addEventListener("click", function () {
            currentImageIndex = index;
            const imageUrl = this.querySelector("img").src;
            currentImageUrl = this.querySelector("img").src;
            const altText = this.querySelector("img").alt;
            globalYoutubeLink = parseAltText(altText);
            const imageName = altText.replace(globalYoutubeLink, "").trim();
            showPopup(imageUrl, imageName);
        });
    });

    popupContainer.addEventListener("click", function (event) {
        if (event.target === popupContainer) {
            hidePopup();
        }
    });

    // Ensure thumbnailList is properly defined
    thumbnailList = document.querySelector(".thumbnail-list");

    function parseAltText(altText) {
        const match = altText.match(/https:\/\/youtu\.be\/[\w-]+(\?.+)?/);
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
    
        const searchIcon = document.createElement("img");
        searchIcon.src = "/static/icons/search_icon.svg"
        searchIcon.alt = "Search";
        searchIcon.className = "search-icon";
        searchIcon.addEventListener("click", function () {
            retrieveImage(imageUrl)
        });
        buttonsContainer.appendChild(searchIcon);
    
        const youtubeIcon = document.createElement("img");
        youtubeIcon.src = "/static/icons/youtube_icon.svg";
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
    
        updateThumbnailList(imageUrl);
    
        document.removeEventListener("keydown", navigateOnKeyPress);
        document.addEventListener("keydown", navigateOnKeyPress);
    }
    
    function hidePopup() {
        popupContainer.style.display = "none";
        document.removeEventListener("keydown", navigateOnKeyPress);
    }

    // function updateThumbnailList(imageUrl) {
    //     thumbnailList.innerHTML = "";
    
    //     const currentNumber = parseInt(currentImageUrl.split('/').pop().split('.')[0], 10);
    //     const directory = currentImageUrl.substring(0, currentImageUrl.lastIndexOf("/"));
    
    //     const maxIndex = currentNumber + 3;
    //     const minIndex = Math.max(1, currentNumber - 3);
    
    //     for (let i = minIndex; i <= maxIndex; i++) {
    //         const paddedNumber = String(i).padStart(4, '0');
    //         const imagePath = `${directory}/${paddedNumber}.jpg`;
    //         if (imageExists(imagePath)) {
    //             const thumbnailItem = document.createElement("div");
    //             thumbnailItem.className = "thumbnail-item";
    //             if (i === currentNumber) {
    //                 thumbnailItem.classList.add("current-thumbnail");
    //             }
    //             const thumbnailImage = document.createElement("img");
    //             thumbnailImage.src = imagePath;
    //             thumbnailImage.alt = getImageName(directory, paddedNumber);
    //             thumbnailImage.addEventListener("click", function(event) {
    //                 showPopup(event.target.src, event.target.alt);
    //             });
    //             thumbnailItem.appendChild(thumbnailImage);
    //             thumbnailList.appendChild(thumbnailItem);
    //         }
    //     }
    // }
    
    function updateThumbnailList(imageUrl) {
        thumbnailList.innerHTML = "";
    
        const currentNumber = parseInt(imageUrl.split('/').pop().split('.')[0], 10);
        const directory = imageUrl.substring(0, imageUrl.lastIndexOf("/"));
    
        const maxIndex = currentNumber + 3;
        const minIndex = Math.max(1, currentNumber - 3);
    
        for (let i = minIndex; i <= maxIndex; i++) {
            const paddedNumber = String(i).padStart(4, '0');
            const imagePath = `${directory}/${paddedNumber}.jpg`;
            if (imageExists(imagePath)) {
                const thumbnailItem = document.createElement("div");
                thumbnailItem.className = "thumbnail-item";
                const thumbnailImage = document.createElement("img");
                thumbnailImage.src = imagePath;
                thumbnailImage.alt = getImageName(directory, paddedNumber);
                thumbnailImage.addEventListener("click", function(event) {
                    showPopup(event.target.src, event.target.alt);
                });
                if (i === currentNumber) {
                    thumbnailItem.classList.add("current-thumbnail");
                }
                thumbnailItem.appendChild(thumbnailImage);
                thumbnailList.appendChild(thumbnailItem);
            }
        }
    }
    

    function getImageName(directory, paddedNumber) {
        const parts = directory.split('/');
        const sequenceName = parts[parts.length - 2];
        const versionNumber = parts[parts.length - 1];
        return `${sequenceName}/${versionNumber}/${paddedNumber}.jpg`;
    }   
    
    function imageExists(imagePath) {
        const http = new XMLHttpRequest();
        http.open('HEAD', imagePath, false);
        http.send();
        return http.status !== 404;
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
            currentImageIndex = (currentImageIndex + direction + imageItems.length) % imageItems.length;
            currentImageUrl = nextImagePath;
            const altText = imageItems[currentImageIndex].querySelector("img").alt;
            globalYoutubeLink = parseAltText(altText);
    
            const popupImage = document.querySelector(".popup-image");
            popupImage.src = currentImageUrl;
            popupImage.alt = nextImageName + globalYoutubeLink;
            document.querySelector(".popup-image-name").innerText = nextImageName;
    
            const buttonsContainer = document.querySelector(".buttons");
            const youtubeIcon = buttonsContainer.querySelector(".youtube-icon");
            youtubeIcon.removeEventListener("click", handleYoutubeIconClick);
            youtubeIcon.addEventListener("click", handleYoutubeIconClick);
    
            updateThumbnailList(currentImageUrl);
        }
    }    

    function handleYoutubeIconClick() {
        if (globalYoutubeLink) {
            window.open(globalYoutubeLink, '_blank');
        } else {
            alert("No YouTube link available for this image.");
        }
    }

    function navigateToThumbnail(index) {
        const thumbnailImagePath = imageItems[index].querySelector("img").src;
        const thumbnailImageName = imageItems[index].querySelector("img").alt;

        document.querySelector(".popup-image").src = thumbnailImagePath;
        document.querySelector(".popup-image-name").innerText = thumbnailImageName;
        currentImageIndex = index;
        updateThumbnailList(thumbnailImagePath); // Pass thumbnailImagePath to updateThumbnailList
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

                const existingResultsContainer = document.querySelector('.container');
                existingResultsContainer.replaceWith(newResultsContainer);

                const Container = document.querySelector('.container');
                Container.style.marginLeft = '2rem';

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
                currentImageUrl = this.querySelector("img").src;
                const altText = this.querySelector("img").alt;
                globalYoutubeLink = parseAltText(altText);
                const imageName = altText.replace(globalYoutubeLink, "").trim();
                showPopup(imageUrl, imageName);
            });
        });
    }

});
