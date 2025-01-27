(function () {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector("body");
    const selectHeader = document.querySelector("#header");
    if (
      !selectHeader.classList.contains("scroll-up-sticky") &&
      !selectHeader.classList.contains("sticky-top") &&
      !selectHeader.classList.contains("fixed-top")
    )
      return;
    window.scrollY > 100
      ? selectBody.classList.add("scrolled")
      : selectBody.classList.remove("scrolled");
  }

  document.addEventListener("scroll", toggleScrolled);
  window.addEventListener("load", toggleScrolled);

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector(".mobile-nav-toggle");

  function mobileNavToogle() {
    document.querySelector("body").classList.toggle("mobile-nav-active");
    mobileNavToggleBtn.classList.toggle("bi-list");
    mobileNavToggleBtn.classList.toggle("bi-x");
  }
  mobileNavToggleBtn.addEventListener("click", mobileNavToogle);

  /**
   * Hide mobile nav on same-page/hash links
   */
  document.querySelectorAll("#navmenu a").forEach((navmenu) => {
    navmenu.addEventListener("click", () => {
      if (
        document.querySelector(".mobile-nav-active") &&
        !navmenu.parentElement.classList.contains("dropdown")
      ) {
        mobileNavToogle();
      }
    });
  });

  /**
   * Toggle mobile nav dropdowns
   */
  const initDropdowns = () => {
    const dropdowns = document.querySelectorAll(".navmenu .dropdown > a");

    dropdowns.forEach((dropdown) => {
      dropdown.addEventListener("click", function (e) {
        if (window.innerWidth <= 1199.98) {
          e.preventDefault();
          e.stopPropagation();

          if (window.innerWidth <= 991.98) {
            dropdowns.forEach((otherDropdown) => {
              if (otherDropdown !== this) {
                otherDropdown.parentElement.classList.remove("active");
              }
            });
          }

          this.parentElement.classList.toggle("active");
        }
      });
    });

    document.addEventListener("click", function (e) {
      if (window.innerWidth <= 1199.98) {
        if (!e.target.closest(".dropdown")) {
          dropdowns.forEach((dropdown) => {
            dropdown.parentElement.classList.remove("active");
          });
        }
      }
    });
  };

  window.addEventListener("load", initDropdowns);

  /**
   * Service Details Content Management
   */
 function initServiceDetails() {
   const servicePage = document.querySelector("[data-service-page]");
   if (!servicePage) return;

   const serviceContentContainer = document.querySelector("#service-content");
   const serviceLinks = document.querySelectorAll(".services-list a");

   const path = window.location.pathname;
   const pathParts = path.split("/").filter(Boolean);
   const slug = pathParts[pathParts.length - 1];

   function updateServiceContent(serviceKey) {
     const service = servicesData[serviceKey];
     if (!service) return;

     const currentBreadcrumb = document.querySelector(".breadcrumbs .current");
     if (currentBreadcrumb) {
       currentBreadcrumb.textContent = service.titre;
     }

     const currentContent =
       serviceContentContainer.querySelector(".service-content");
     if (currentContent) {
       currentContent.style.opacity = "0";
     }

     setTimeout(() => {
       serviceContentContainer.innerHTML = `
        <div class="service-content">
          <img src="${service.image}" alt="${service.titre}" class="img-fluid services-img">
          ${service.grande_description}
        </div>
      `;

       const newContent =
         serviceContentContainer.querySelector(".service-content");
       newContent.offsetHeight;

       requestAnimationFrame(() => {
         newContent.style.opacity = "1";
       });
     }, 300);

     serviceLinks.forEach((link) => link.classList.remove("active"));
     const activeLink = document.querySelector(
       `[data-service="${serviceKey}"]`
     );
     if (activeLink) activeLink.classList.add("active");
   }

   serviceLinks.forEach((link) => {
     link.addEventListener("click", (e) => {
       const serviceKey = link.getAttribute("data-service");
       updateServiceContent(serviceKey);
       if (history.pushState) {
         window.history.pushState(null, "", link.href);
       }
     });
   });

   if (slug && servicesData[slug]) {
     updateServiceContent(slug);
   } else {
     const firstServiceKey = serviceLinks[0]?.getAttribute("data-service");
     if (firstServiceKey) updateServiceContent(firstServiceKey);
   }
 }

  window.addEventListener("load", initServiceDetails);

  /**
   * Preloader
   */
  const preloader = document.querySelector("#preloader");
  if (preloader) {
    window.addEventListener("load", () => {
      preloader.remove();
    });
  }

  /**
   * Scroll top button
   */
  let scrollTop = document.querySelector(".scroll-top");

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100
        ? scrollTop.classList.add("active")
        : scrollTop.classList.remove("active");
    }
  }
  scrollTop.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  });

  window.addEventListener("load", toggleScrollTop);
  document.addEventListener("scroll", toggleScrollTop);

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: "ease-in-out",
      once: true,
      mirror: false,
    });
  }
  window.addEventListener("load", aosInit);

  /**
   * Initiate glightbox
   */
  const glightbox = GLightbox({
    selector: ".glightbox",
  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function (swiperElement) {
      let config = JSON.parse(
        swiperElement.querySelector(".swiper-config").innerHTML.trim()
      );

      if (swiperElement.classList.contains("swiper-tab")) {
        initSwiperWithCustomPagination(swiperElement, config);
      } else {
        new Swiper(swiperElement, config);
      }
    });
  }

  window.addEventListener("load", initSwiper);

  /**
   * Init isotope layout and filters
   */
  document.querySelectorAll(".isotope-layout").forEach(function (isotopeItem) {
    let layout = isotopeItem.getAttribute("data-layout") ?? "masonry";
    let filter = isotopeItem.getAttribute("data-default-filter") ?? "*";
    let sort = isotopeItem.getAttribute("data-sort") ?? "original-order";

    let initIsotope;
    imagesLoaded(isotopeItem.querySelector(".isotope-container"), function () {
      initIsotope = new Isotope(
        isotopeItem.querySelector(".isotope-container"),
        {
          itemSelector: ".isotope-item",
          layoutMode: layout,
          filter: filter,
          sortBy: sort,
        }
      );
    });

    isotopeItem
      .querySelectorAll(".isotope-filters li")
      .forEach(function (filters) {
        filters.addEventListener(
          "click",
          function () {
            isotopeItem
              .querySelector(".isotope-filters .filter-active")
              .classList.remove("filter-active");
            this.classList.add("filter-active");
            initIsotope.arrange({
              filter: this.getAttribute("data-filter"),
            });
            if (typeof aosInit === "function") {
              aosInit();
            }
          },
          false
        );
      });
  });
})();
