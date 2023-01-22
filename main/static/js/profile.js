const posts = document.querySelectorAll('.gallery-item');

posts.forEach(post => {
	post.addEventListener('click', () => {
		const imgUrl = post.firstElementChild.src.split("?")[0];
		window.open(imgUrl, '_blank');
	});
});

