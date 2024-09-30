function addCaptions() {
	document.querySelectorAll("img").forEach((e) => {
		let caption = e.alt;

		// Create p element containg the alt-text
		let captionElement = document.createElement("p");
		captionElement.innerHTML = caption;
		captionElement.classList = "caption";

		let parent = e.parentNode;
		parent.appendChild(captionElement);
	});
};

addCaptions();