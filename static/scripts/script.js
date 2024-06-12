document.addEventListener('DOMContentLoaded', () => {
    const booksPerPage = 4;
    let currentPage = 1;
    let books = [];
    let currentCatalog = 'All';

    const gridContainer = document.getElementById('grid-container');
    const paginationContainer = document.getElementById('pagination');

    async function fetchBooks(catalog = 'All') {
        try {
            const response = await fetch(`/api/books?catalog=${catalog}`);
            const data = await response.json();
            if (data.error) {
                console.error(data.error);
                return;
            }
            books = data.books;
            renderPage(currentPage);
        } catch (error) {
            console.error('Error fetching books:', error);
        }
    }

    function renderPage(page) {
        gridContainer.innerHTML = '';
        const start = (page - 1) * booksPerPage;
        const end = start + booksPerPage;
        const booksToRender = books.slice(start, end);

        booksToRender.forEach(book => {
            const card = document.createElement('div');
            card.className = 'card';
            card.innerHTML = `
                <div>
                    <img src="${book.image}" alt="${book.title}">
                </div>
                <div>
                    <p>${book.title}</p>
                    <a href="${book.downloadLink}" download><button>Download</button></a>
                    <a href="${book.readOnlineLink}" target="_blank"><button>Read Online</button></a>
                </div>
                <div>
                    <p>Author: ${book.author}</p>
                    <p>Rating: ${book.rating}</p>
                </div>
            `;
            gridContainer.appendChild(card);
        });

        updatePagination(page);
    }

    function updatePagination(activePage) {
        paginationContainer.innerHTML = '';
        const totalPages = Math.ceil(books.length / booksPerPage);

        for (let i = 1; i <= totalPages; i++) {
            const pageButton = document.createElement('button');
            pageButton.textContent = i;
            if (i === activePage) {
                pageButton.classList.add('active');
            }
            pageButton.addEventListener('click', () => {
                currentPage = i;
                renderPage(currentPage);
            });
            paginationContainer.appendChild(pageButton);
        }
    }

    window.filterBooks = function(catalog) {
        currentCatalog = catalog;
        currentPage = 1;
        fetchBooks(currentCatalog);
    }

    fetchBooks();
});
