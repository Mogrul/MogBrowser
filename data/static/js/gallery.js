const sidebar = document.getElementById("sidebar");
const mediaCards = document.getElementsByClassName("path-card");

document.addEventListener("DOMContentLoaded", async (event) => {
    await loadMediaCards();
});

function sidebarOpen() {
    sidebar.style.display = "block";
}

function sidebarClose() {
    sidebar.style.display = "none";
}

async function loadMediaCards() {
    const paths = [];

    for (const mediaCard of mediaCards) {
        const pathName = mediaCard.dataset.pathName;
        const pathType = mediaCard.dataset.pathType;

        if (pathType === "video" || pathType === "image") {
            paths.push(pathName);
        }
    }

    if (paths.length === 0) return;

    const response = await requestThumbnails(paths);
    console.log(response);
}

async function requestThumbnails(paths) {
    const response = await fetch("/media/thumbnail", {
        method: "POST",
        "headers": {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            "scope": currentScope,
            "paths": paths
        })
    });

    if (!response.ok) {
        throw new Error(`Thumbnail request failed: ${response.status}`);
    }

    return await response.json();
}