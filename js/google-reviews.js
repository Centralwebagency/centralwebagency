  const placeId = "ChIJKUWum2ezmqQR5SG-AafOKJ8";  // on va le récupérer ensemble
  const apiKey = "AIzaSyC2GdBp6jv8y0Gy00VwixhOaLMI2UvOzC0";     // celle que tu viens de créer

  fetch(`https://maps.googleapis.com/maps/api/place/details/json?place_id=${placeId}&fields=name,rating,reviews&key=${apiKey}`)
    .then(response => response.json())
    .then(data => {
      const reviews = data.result.reviews || [];
      let html = "";
      reviews.forEach(r => {
        html += `
          <div class="review">
            <p><strong>${r.author_name}</strong> — ★${r.rating}</p>
            <p>${r.text}</p>
          </div>`;
      });
      document.querySelector(".ti-widget").innerHTML = html;
    })
    .catch(err => console.error("Erreur API Google :", err));
