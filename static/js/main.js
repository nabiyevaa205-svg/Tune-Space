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
    const toggleBtns = document.querySelectorAll('[data-action="toggle"]');
    const backBtn = document.querySelector('[data-action="back"]');
    const forwardBtn = document.querySelector('[data-action="forward"]');
    const wave = document.getElementById("audio-wave");
    const currentEl = document.getElementById("audio-current");
    const durationEl = document.getElementById("audio-duration");
    const progressFill = document.getElementById("audio-progress-fill");
    const volumeInput = document.getElementById("audio-volume");
    const playPage = document.querySelector(".play-page");
    const previewTitle = player.dataset.previewTitle || "";
    const previewArtist = player.dataset.previewArtist || "";
    const localSrc = player.dataset.localSrc || "";
    let previewLoaded = false;

    const format = (sec) => {
      if (!Number.isFinite(sec)) return "00:00";
      const m = Math.floor(sec / 60).toString().padStart(2, "0");
      const s = Math.floor(sec % 60).toString().padStart(2, "0");
      return `${m}:${s}`;
    };

    const updateTime = () => {
      const current = format(player.currentTime);
      const duration = format(player.duration);
      if (timeEl) timeEl.textContent = `${current} / ${duration}`;
      if (currentEl) currentEl.textContent = current;
      if (durationEl) durationEl.textContent = duration;
      if (progressFill) {
        const progress = player.duration ? (player.currentTime / player.duration) * 100 : 0;
        progressFill.style.width = `${Math.min(100, Math.max(0, progress))}%`;
      }
    };

    const setToggleLabels = (isPlaying) => {
      const playIcon = '<svg class="ts-icon" viewBox="0 0 24 24" aria-hidden="true"><polygon points="6 3 20 12 6 21 6 3"></polygon></svg>';
      const pauseIcon = '<svg class="ts-icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>';
      toggleBtns.forEach((btn) => {
        const playLabel = btn.dataset.playLabel || "Play";
        const pauseLabel = btn.dataset.pauseLabel || "Pause";
        btn.innerHTML = isPlaying ? pauseIcon : playIcon;
        btn.classList.toggle("is-playing", isPlaying);
        btn.setAttribute("aria-label", isPlaying ? pauseLabel : playLabel);
      });
      playPage?.classList.toggle("is-playing", isPlaying);
    };

    player.addEventListener("loadedmetadata", updateTime);
    player.addEventListener("timeupdate", updateTime);

    const loadInternetPreview = async () => {
      if (previewLoaded || player.currentSrc) return true;
      const query = encodeURIComponent(`${previewArtist} ${previewTitle}`);
      try {
        const res = await fetch(`https://itunes.apple.com/search?term=${query}&entity=song&limit=1`);
        if (res.ok) {
          const data = await res.json();
          const previewUrl = data.results?.[0]?.previewUrl;
          if (previewUrl) {
            player.src = previewUrl;
            previewLoaded = true;
            player.load();
            return true;
          }
        }
      } catch (err) {
        // Fall back to a local file if the browser cannot reach the preview API.
      }

      if (localSrc) {
        player.src = localSrc;
        previewLoaded = true;
        player.load();
        return true;
      }
      return false;
    };

    if (volumeInput) {
      const syncVolume = () => {
        const volume = Number(volumeInput.value);
        player.volume = Number.isFinite(volume) ? volume : 0.72;
        volumeInput.style.background = `linear-gradient(90deg, #ffffff ${player.volume * 100}%, rgba(255, 255, 255, 0.22) ${player.volume * 100}%)`;
      };

      syncVolume();
      volumeInput.addEventListener("input", syncVolume);
    }

    toggleBtns.forEach((toggleBtn) => {
      toggleBtn.addEventListener("click", async () => {
        if (player.paused) {
          const hasAudio = await loadInternetPreview();
          if (!hasAudio) return;
          try {
            await player.play();
            setToggleLabels(true);
            wave?.classList.add("is-playing");
          } catch (err) {
            setToggleLabels(false);
            wave?.classList.remove("is-playing");
          }
        } else {
          player.pause();
          setToggleLabels(false);
          wave?.classList.remove("is-playing");
        }
      });
    });

    backBtn?.addEventListener("click", () => {
      player.currentTime = Math.max(0, player.currentTime - 10);
    });

    forwardBtn?.addEventListener("click", () => {
      player.currentTime = Math.min(player.duration || player.currentTime + 10, player.currentTime + 10);
    });

    player.addEventListener("ended", () => {
      setToggleLabels(false);
      wave?.classList.remove("is-playing");
    });
  }

  document.querySelectorAll('[data-action="shuffle"], [data-action="save"]').forEach((button) => {
    button.addEventListener("click", () => {
      button.classList.toggle("active");
      button.setAttribute("aria-pressed", button.classList.contains("active") ? "true" : "false");
    });
  });

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
    let img = node.querySelector("img");
    if (!artist || !title) return;
    if (!img) {
      const placeholder = node.querySelector(".mini-thumb, .cover-placeholder");
      if (!placeholder) return;
      img = document.createElement("img");
      img.alt = title;
      if (placeholder.classList.contains("cover-placeholder")) {
        img.className = placeholder.className
          .toString()
          .replace(/\bcover-placeholder\b/g, "")
          .trim() || "play-cover";
      }
      placeholder.replaceWith(img);
    }

    const cacheKey = `${artist} ${title}`.toLowerCase();
    const cached = artworkCache.get(cacheKey);
    if (cached) {
      img.src = cached;
      return;
    }

    try {
      const query = encodeURIComponent(`${artist} ${title}`);
      const res = await fetch(`https://itunes.apple.com/search?term=${query}&entity=song&country=US&limit=1`);
      if (!res.ok) return;
      const data = await res.json();
      const artwork = data.results?.[0]?.artworkUrl100;
      if (!artwork) return;

      const highResArtwork = artwork.replace("100x100bb", "1000x1000bb");
      artworkCache.set(cacheKey, highResArtwork);
      img.src = highResArtwork;
    } catch (err) {
      // Keep the local fallback cover if artwork lookup is unavailable.
    }
  });

  const artistPhotoCache = new Map();
  document.querySelectorAll("[data-artist-photo]").forEach(async (img) => {
    const artist = img.dataset.artistPhoto || "";
    if (!artist) return;

    const cacheKey = artist.toLowerCase();
    const cached = artistPhotoCache.get(cacheKey);
    if (cached) {
      img.src = cached;
      return;
    }

    try {
      const title = encodeURIComponent(artist.replace(/\s+/g, "_"));
      const res = await fetch(`https://en.wikipedia.org/api/rest_v1/page/summary/${title}`);
      if (!res.ok) return;
      const data = await res.json();
      const photo = data.thumbnail?.source || data.originalimage?.source;
      if (!photo) return;

      artistPhotoCache.set(cacheKey, photo);
      img.src = photo;
    } catch (err) {
      // Keep the server-side fallback image if Wikipedia does not return a photo.
    }
  });

  const songSearch = document.querySelector("[data-song-search]");
  const songGrid = document.querySelector("[data-song-grid]");
  const songSearchEmpty = document.querySelector("[data-song-search-empty]");

  if (songSearch && songGrid) {
    const cards = Array.from(songGrid.querySelectorAll(".song-card"));
    const filterSongs = () => {
      const query = songSearch.value.trim().toLowerCase();
      let visibleCount = 0;

      cards.forEach((card) => {
        const haystack = [
          card.dataset.track || "",
          card.dataset.artist || "",
          card.dataset.description || "",
        ].join(" ");
        const isVisible = !query || haystack.includes(query);
        card.hidden = !isVisible;
        if (isVisible) visibleCount += 1;
      });

      if (songSearchEmpty) {
        songSearchEmpty.hidden = visibleCount !== 0;
      }
    };

    songSearch.addEventListener("input", filterSongs);
    filterSongs();
  }

  const menuToggle = document.querySelector("[data-menu-toggle]");
  const menuClose = document.querySelector("[data-menu-close]");
  const mainNav = document.getElementById("main-navigation");
  const desktopMenu = document.getElementById("desktop-menu");

  if (menuToggle && mainNav) {
    const setMenuOpen = (isOpen) => {
      document.body.classList.toggle("menu-open", isOpen);
      menuToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    };

    menuToggle.addEventListener("click", () => {
      setMenuOpen(!document.body.classList.contains("menu-open"));
    });

    menuClose?.addEventListener("click", () => setMenuOpen(false));

    mainNav.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setMenuOpen(false));
    });

    desktopMenu?.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setMenuOpen(false));
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape") setMenuOpen(false);
    });
  }

  const settingsLinks = document.querySelectorAll(".settings-sidebar a[href^='#']");
  const settingsSections = Array.from(settingsLinks)
    .map((link) => document.querySelector(link.getAttribute("href")))
    .filter(Boolean);

  settingsLinks.forEach((link) => {
    link.addEventListener("click", () => {
      settingsLinks.forEach((item) => item.classList.remove("active"));
      link.classList.add("active");
    });
  });

  if (settingsLinks.length && "IntersectionObserver" in window) {
    const sectionObserver = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (!visible) return;

        settingsLinks.forEach((link) => {
          link.classList.toggle("active", link.getAttribute("href") === `#${visible.target.id}`);
        });
      },
      { rootMargin: "-30% 0px -55% 0px", threshold: [0.12, 0.35, 0.6] }
    );

    settingsSections.forEach((section) => sectionObserver.observe(section));
  }

});
