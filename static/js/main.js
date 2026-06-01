document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".reveal");
  cards.forEach((card, i) => {
    setTimeout(() => card.classList.add("visible"), 110 * i);
  });

  const form = document.getElementById("auth-form");
  if (form) {
    form.addEventListener("submit", (e) => {
      const requiredInputs = form.querySelectorAll("input[required]");
      let valid = true;
      requiredInputs.forEach((inp) => {
        if (!inp.value.trim()) {
          valid = false;
          inp.style.border = "1px solid #ff6d6d";
        }
      });
      if (!valid) {
        e.preventDefault();
        alert("Please fill in all required fields.");
      }
    });
  }

  const player = document.getElementById("audio-player");
  if (player) {
    const timeEl = document.getElementById("audio-time");
    const toggleBtn = document.querySelector('[data-action="toggle"]');
    const backBtn = document.querySelector('[data-action="back"]');
    const forwardBtn = document.querySelector('[data-action="forward"]');
    const wave = document.getElementById("audio-wave");

    const format = (sec) => {
      if (!Number.isFinite(sec)) return "00:00";
      const m = Math.floor(sec / 60).toString().padStart(2, "0");
      const s = Math.floor(sec % 60).toString().padStart(2, "0");
      return `${m}:${s}`;
    };

    const updateTime = () => {
      if (timeEl) timeEl.textContent = `${format(player.currentTime)} / ${format(player.duration)}`;
    };

    player.addEventListener("loadedmetadata", updateTime);
    player.addEventListener("timeupdate", updateTime);

    toggleBtn?.addEventListener("click", async () => {
      const playLabel = toggleBtn.dataset.playLabel || "Play";
      const pauseLabel = toggleBtn.dataset.pauseLabel || "Pause";
      if (player.paused) {
        await player.play();
        toggleBtn.textContent = pauseLabel;
        wave?.classList.add("is-playing");
      } else {
        player.pause();
        toggleBtn.textContent = playLabel;
        wave?.classList.remove("is-playing");
      }
    });

    backBtn?.addEventListener("click", () => {
      player.currentTime = Math.max(0, player.currentTime - 10);
    });

    forwardBtn?.addEventListener("click", () => {
      player.currentTime = Math.min(player.duration || player.currentTime + 10, player.currentTime + 10);
    });

    player.addEventListener("ended", () => {
      if (toggleBtn) toggleBtn.textContent = toggleBtn.dataset.playLabel || "Play";
      wave?.classList.remove("is-playing");
    });
  }

  document.querySelectorAll(".artist-follow-btn").forEach((followBtn) => {
    const artist = followBtn.dataset.followArtist || "artist";
    const storageKey = `tunespace-follow-${artist.toLowerCase().replace(/\s+/g, "-")}`;
    const followLabel = followBtn.dataset.followLabel || "Follow";
    const followingLabel = followBtn.dataset.followingLabel || "Following";

    const setFollowState = (isFollowing) => {
      followBtn.classList.toggle("is-following", isFollowing);
      followBtn.textContent = isFollowing ? followingLabel : followLabel;
      followBtn.setAttribute("aria-pressed", isFollowing ? "true" : "false");
    };

    setFollowState(localStorage.getItem(storageKey) === "1");

    followBtn.addEventListener("click", () => {
      const nextState = !followBtn.classList.contains("is-following");
      localStorage.setItem(storageKey, nextState ? "1" : "0");
      setFollowState(nextState);
    });
  });

  const artworkCache = new Map();
  const artworkNodes = document.querySelectorAll("[data-artwork-title]");

  artworkNodes.forEach(async (node) => {
    const artist = node.dataset.artworkArtist || "";
    const title = node.dataset.artworkTitle || "";
    const img = node.querySelector("img");
    if (!artist || !title || !img) return;

    const cacheKey = `${artist} ${title}`.toLowerCase();
    const cached = artworkCache.get(cacheKey);
    if (cached) {
      img.src = cached;
      return;
    }

    try {
      const query = encodeURIComponent(`${artist} ${title}`);
      const res = await fetch(`https://itunes.apple.com/search?term=${query}&entity=song&limit=1`);
      if (!res.ok) return;
      const data = await res.json();
      const artwork = data.results?.[0]?.artworkUrl100;
      if (!artwork) return;

      const highResArtwork = artwork.replace("100x100bb", "600x600bb");
      artworkCache.set(cacheKey, highResArtwork);
      img.src = highResArtwork;
    } catch (err) {
      // Keep the local fallback cover if artwork lookup is unavailable.
    }
  });
  
});
