// Tutorial System
class Tutorial {
    constructor() {
        this.steps = [
            {
                title: "Welcome to Invoice System! 👋",
                message: "Let's take a quick tour to help you get started. This tutorial will guide you through the main features.",
                element: null,
                position: "center"
            },
            {
                title: "Step 1: Customers",
                message: "Start by adding your customers here. You'll need customers before creating invoices.",
                element: "a[href*='customer']",
                action: "Click 'All Customers' or 'Add Customer' in the sidebar"
            },
            {
                title: "Step 2: Inventory",
                message: "Next, set up your inventory. Create categories and add items with prices and stock quantities.",
                element: "a[href*='item']",
                action: "Go to 'Categories' or 'All Items' in the sidebar"
            },
            {
                title: "Step 3: Create Invoices",
                message: "Now you can create invoices! Select a customer, add items, and the system will auto-generate invoice numbers.",
                element: "a[href*='invoice']",
                action: "Click 'Create Invoice' to get started"
            },
            {
                title: "Step 4: Record Payments",
                message: "When customers pay, record it here. The system will automatically update invoice status and reduce inventory.",
                element: "a[href*='payment']",
                action: "Use 'Record Payment' to track payments"
            },
            {
                title: "You're All Set! 🎉",
                message: "You now know the basics! Explore the sidebar for more features. Click 'Start Tutorial' anytime to see this again.",
                element: null,
                position: "center"
            }
        ];
        this.currentStep = 0;
        this.overlay = null;
        this.modal = null;
    }

    start() {
        this.currentStep = 0;
        this.createOverlay();
        this.showStep();
    }

    createOverlay() {
        // Create dark overlay
        this.overlay = document.createElement('div');
        this.overlay.className = 'fixed inset-0 bg-black bg-opacity-50 z-50 transition-opacity';
        this.overlay.style.opacity = '0';
        document.body.appendChild(this.overlay);
        setTimeout(() => this.overlay.style.opacity = '1', 10);

        // Create modal
        this.modal = document.createElement('div');
        this.modal.id = 'tutorial-modal';
        this.modal.className = 'fixed z-50 bg-white rounded-lg shadow-2xl max-w-md w-full p-6 transition-all';
        this.modal.style.opacity = '0';
        this.modal.style.position = 'fixed';
        this.modal.style.bottom = '20px';
        this.modal.style.right = '20px';
        this.modal.style.top = 'auto';
        this.modal.style.left = 'auto';
        this.modal.style.transform = 'scale(0.9)';
        this.modal.style.maxWidth = '400px';
        document.body.appendChild(this.modal);
        setTimeout(() => {
            this.modal.style.opacity = '1';
            this.modal.style.transform = 'scale(1)';
        }, 10);
    }

    showStep() {
        const step = this.steps[this.currentStep];

        // Always position modal at bottom-right - maintain fixed position
        if (this.modal) {
            this.modal.style.position = 'fixed';
            this.modal.style.bottom = '20px';
            this.modal.style.right = '20px';
            this.modal.style.top = 'auto';
            this.modal.style.left = 'auto';
            this.modal.style.transform = 'scale(1)';
            this.modal.style.maxWidth = '400px';
        }

        // Highlight element if it exists
        if (step.element) {
            const el = document.querySelector(step.element);
            if (el) {
                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                // Highlight element with green color
                el.style.outline = '4px solid rgba(13, 181, 97, 0.5)';
                el.style.outlineOffset = '2px';
                setTimeout(() => {
                    el.style.outline = '';
                    el.style.outlineOffset = '';
                }, 3000);
            }
        }

        // Update modal content
        this.modal.innerHTML = `
            <div class="space-y-4">
                <div class="flex items-start justify-between">
                    <h3 class="text-xl font-bold text-gray-900">${step.title}</h3>
                    <button onclick="tutorial.end()" class="text-gray-400 hover:text-gray-600">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                    </button>
                </div>
                <p class="text-gray-600">${step.message}</p>
                ${step.action ? `<p class="text-sm font-medium" style="color: #0DB561;">💡 ${step.action}</p>` : ''}
                <div class="flex items-center justify-between pt-4 border-t">
                    <div class="flex space-x-1">
                        ${this.steps.map((_, i) => `
                            <div class="w-2 h-2 rounded-full ${i === this.currentStep ? '' : 'bg-gray-300'}" style="${i === this.currentStep ? 'background-color: #0DB561;' : ''}"></div>
                        `).join('')}
                    </div>
                    <div class="flex space-x-2">
                        ${this.currentStep > 0 ? `
                            <button onclick="tutorial.prev()" class="px-4 py-2 text-gray-600 hover:text-gray-800">
                                Previous
                            </button>
                        ` : ''}
                        ${this.currentStep < this.steps.length - 1 ? `
                            <button onclick="tutorial.next()" class="px-4 py-2 text-white rounded-md btn-primary">
                                Next
                            </button>
                        ` : `
                            <button onclick="tutorial.end()" class="px-4 py-2 text-white rounded-md btn-primary">
                                Get Started!
                            </button>
                        `}
                    </div>
                </div>
            </div>
        `;
    }

    centerModal() {
        // Keep modal at bottom-right - maintain fixed position
        if (this.modal) {
            this.modal.style.position = 'fixed';
            this.modal.style.bottom = '20px';
            this.modal.style.right = '20px';
            this.modal.style.top = 'auto';
            this.modal.style.left = 'auto';
            this.modal.style.transform = 'scale(1)';
            this.modal.style.maxWidth = '400px';
        }
    }

    next() {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            this.showStep();
        }
    }

    prev() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.showStep();
        }
    }

    end() {
        if (this.overlay) this.overlay.style.opacity = '0';
        if (this.modal) {
            this.modal.style.opacity = '0';
            this.modal.style.transform = 'scale(0.9)';
        }
        setTimeout(() => {
            if (this.overlay) this.overlay.remove();
            if (this.modal) this.modal.remove();
            localStorage.setItem('tutorialCompleted', 'true');
        }, 300);
    }
}

// Initialize tutorial
const tutorial = new Tutorial();

// Auto-start tutorial for first-time users
document.addEventListener('DOMContentLoaded', function () {
    if (!localStorage.getItem('tutorialCompleted') && document.querySelector('#sidebar')) {
        setTimeout(() => {
            if (confirm('Welcome! Would you like a quick tutorial to get started?')) {
                tutorial.start();
            } else {
                localStorage.setItem('tutorialCompleted', 'true');
            }
        }, 1000);
    }
});

// Global function to start tutorial
function startTutorial() {
    tutorial.start();
}

// Export for global use
window.tutorial = tutorial;
window.startTutorial = startTutorial;
