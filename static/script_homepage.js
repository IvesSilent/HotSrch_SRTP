//搜索页hotsrch_homepage.html脚本
// 事件监听函：点击按钮searchHot触发搜索
document.getElementById('searchHot').addEventListener('click', function () {
    const keyword = document.getElementById('searchInput').value;
    fetch(`/search_hotels?query=${encodeURIComponent(keyword)}`)
        .then(response => response.json())
        .then(hotels => {
            displayHotels(hotels);
        })
//        错误捕获
        .catch(error => console.error('Error:', error));
});

function displayHotels(hotelsToDisplay) {
    const hotelListDiv = document.getElementById('hotelList');
    hotelListDiv.innerHTML = '';
    let currentRow = null;
    for (let i = 0; i < hotelsToDisplay.length; i++) {
        if (i % 3 === 0) {
            currentRow = document.createElement('div');
            currentRow.classList.add('hotel-row');
            hotelListDiv.appendChild(currentRow);
        }
        const hotel = hotelsToDisplay[i];
        const hotelCard = document.createElement('div');
        hotelCard.classList.add('hotel-card');
        hotelCard.innerHTML = `<div class="hotel-info"><h2>${hotel.name}</h2><div class="score-box"><p>${hotel.score}</p></div></div><img src="${hotel.image}" alt="${hotel.name}">`;
        hotelCard.addEventListener('click', () => {
            // 点击酒店卡片时，跳转到酒店详情页
            // 确保使用 encodeURIComponent 对 hotel 对象进行编码
            window.location.href = `/hotsrch_detail?hotel=${encodeURIComponent(JSON.stringify(hotel))}`;
        });
        currentRow.appendChild(hotelCard);
    }
}