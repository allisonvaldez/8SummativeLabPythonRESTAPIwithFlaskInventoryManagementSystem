//Script file for connecting backend and frontend 

// Fetch all existing events from Flask on page load and render them
fetch("http://localhost:5555/events")
  .then(response => response.json())  // Parse the JSON array
  .then(events => {
    events.forEach(renderEvent);      // Render each event as a <li>
  });

// Handle form submission to add a new event
document.querySelector("form").addEventListener("submit", (e) => {
  e.preventDefault();  // Prevent page reload
  // Get value from #title input
  const title = document.querySelector("#title").value;

  // POST to Flask — port 5555 matches server.py
  fetch("http://localhost:5555/events", {  
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title }) 
  })
  // Parse the new event from the response
  .then(response => response.json())  
  .then(renderEvent);
});

// Creates the list and appends new items 
function renderEvent(event) {
  const li = document.createElement("li");
  li.textContent = event.title;
  document.querySelector("#event-list").appendChild(li);
}