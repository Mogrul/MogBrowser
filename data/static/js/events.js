const events = new EventSource("/events");

let clientId = null;

events.onopen = () => {
    console.log("SSE connection opened");
};

events.addEventListener("ready", (event) => {
    console.log("Ready event received:", event.data);

    clientId = JSON.parse(event.data).client;
    console.log("Connected client:", clientId);
});

events.onmessage = (event) => {
    console.log("Message received:", event.data);
};

events.onerror = (event) => {
    console.error("SSE connection error:", event);
    console.log("Ready state:", events.readyState);
};