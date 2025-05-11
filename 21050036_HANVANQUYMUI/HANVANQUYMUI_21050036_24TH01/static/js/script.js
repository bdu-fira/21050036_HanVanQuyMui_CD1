// Common JavaScript functions for the application

// Format currency
function formatCurrency(amount) {
  return Number.parseFloat(amount).toFixed(2)
}

// Confirm delete
function confirmDelete(message) {
  return confirm(message || "Are you sure you want to delete this item?")
}

// Initialize tooltips and popovers
document.addEventListener("DOMContentLoaded", () => {
  // Initialize tooltips
  const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // Initialize popovers
  const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  popoverTriggerList.map((popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl))

  // Auto-dismiss alerts
  setTimeout(() => {
    const alerts = document.querySelectorAll(".alert")
    alerts.forEach((alert) => {
      const bsAlert = new bootstrap.Alert(alert)
      bsAlert.close()
    })
  }, 5000)

  // Set active nav item based on current URL
  const currentPath = window.location.pathname
  const navLinks = document.querySelectorAll("#sidebar .nav-link")

  navLinks.forEach((link) => {
    const href = link.getAttribute("href")
    if (currentPath === href || (currentPath.startsWith(href) && href !== "/")) {
      link.classList.add("active")
      link.style.backgroundColor = "rgba(255, 255, 255, 0.2)"
    }
  })
})

// Fetch product details
async function getProductDetails(productId) {
  try {
    const response = await fetch(`/api/products/${productId}`)
    if (!response.ok) {
      throw new Error("Failed to fetch product details")
    }
    return await response.json()
  } catch (error) {
    console.error("Error:", error)
    return null
  }
}

// Fetch category attributes
async function getCategoryAttributes(categoryId) {
  try {
    const response = await fetch(`/api/categories/${categoryId}/attributes`)
    if (!response.ok) {
      throw new Error("Failed to fetch category attributes")
    }
    return await response.json()
  } catch (error) {
    console.error("Error:", error)
    return []
  }
}

// Search functionality
function setupSearch(inputId, itemSelector, nameAttribute = "data-name") {
  const searchInput = document.getElementById(inputId)
  if (!searchInput) return

  searchInput.addEventListener("input", function () {
    const searchTerm = this.value.toLowerCase()
    const items = document.querySelectorAll(itemSelector)

    items.forEach((item) => {
      const name = item.getAttribute(nameAttribute).toLowerCase()
      if (name.includes(searchTerm)) {
        item.style.display = ""
      } else {
        item.style.display = "none"
      }
    })
  })
}
