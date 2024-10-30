//����ҳhotsrch_homepage.html�ű�
// �¼��������������ťsearchHot��������
document.getElementById('searchHot').addEventListener('click', function () {
    const keyword = document.getElementById('searchInput').value;
    fetch(`/search_hotels?query=${encodeURIComponent(keyword)}`)
        .then(response => response.json())
        .then(hotels => {
            displayHotels(hotels);
        })
//        ���󲶻�
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
            // ����Ƶ꿨Ƭʱ����ת���Ƶ�����ҳ
            // ȷ��ʹ�� encodeURIComponent �� hotel ������б���
            window.location.href = `/hotsrch_detail?hotel=${encodeURIComponent(JSON.stringify(hotel))}`;
        });
        currentRow.appendChild(hotelCard);
    }
}