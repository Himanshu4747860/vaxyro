
// Enhanced Vaxyro Platform JavaScript

// Tool metadata for featured tools
const featuredToolsData = [
  {
    id: 'vulnscan',
    name: 'AI Vulnerability Scanner',
    description: 'AI-powered comprehensive vulnerability assessment',
    icon: '🤖',
    gradient: 'from-pink-400 to-rose-500'
  },
  {
    id: 'sqlmap',
    name: 'SQL Injection Tester',
    description: 'Advanced SQL injection detection and exploitation',
    icon: '💉',
    gradient: 'from-red-400 to-pink-500'
  },
  {
    id: 'aircrack',
    name: 'WiFi Security Tester',
    description: 'Professional WiFi security auditing tool',
    icon: '📶',
    gradient: 'from-blue-400 to-cyan-500'
  },
  {
    id: 'subdomain',
    name: 'Subdomain Finder',
    description: 'Advanced subdomain enumeration and discovery',
    icon: '🔍',
    gradient: 'from-green-400 to-blue-500'
  },
  {
    id: 'portscan',
    name: 'Advanced Port Scanner',
    description: 'High-speed multi-threaded port scanning',
    icon: '🔌',
    gradient: 'from-purple-400 to-blue-500'
  },
  {
    id: 'firewall',
    name: 'Firewall Bypass Tester',
    description: 'Advanced firewall detection and bypass testing',
    icon: '🔥',
    gradient: 'from-orange-400 to-red-500'
  }
];

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
  initializeBackgroundAnimation();
  initializeSidebarFunctionality();
  initializeSearch();
  populateFeaturedTools();
  initializeTerminal();
  
  // Add smooth scrolling to all anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
});

// Background Animation
function initializeBackgroundAnimation() {
  const canvas = document.getElementById('bg');
  const ctx = canvas.getContext('2d');
  
  let particles = [];
  const particleCount = window.innerWidth < 768 ? 50 : 100;
  
  function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  
  resizeCanvas();
  window.addEventListener('resize', resizeCanvas);
  
  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.vx = (Math.random() - 0.5) * 0.5;
      this.vy = (Math.random() - 0.5) * 0.5;
      this.size = Math.random() * 2 + 0.5;
      this.opacity = Math.random() * 0.5 + 0.2;
    }
    
    update() {
      this.x += this.vx;
      this.y += this.vy;
      
      if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
      if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
      
      this.opacity += (Math.random() - 0.5) * 0.01;
      this.opacity = Math.max(0.1, Math.min(0.8, this.opacity));
    }
    
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0, 245, 255, ${this.opacity})`;
      ctx.fill();
    }
  }
  
  for (let i = 0; i < particleCount; i++) {
    particles.push(new Particle());
  }
  
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach(particle => {
      particle.update();
      particle.draw();
    });
    
    // Draw connections between nearby particles
    particles.forEach((particle, i) => {
      particles.slice(i + 1).forEach(otherParticle => {
        const distance = Math.sqrt(
          Math.pow(particle.x - otherParticle.x, 2) +
          Math.pow(particle.y - otherParticle.y, 2)
        );
        
        if (distance < 100) {
          ctx.beginPath();
          ctx.moveTo(particle.x, particle.y);
          ctx.lineTo(otherParticle.x, otherParticle.y);
          ctx.strokeStyle = `rgba(139, 92, 246, ${0.1 * (1 - distance / 100)})`;
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }
      });
    });
    
    requestAnimationFrame(animate);
  }
  
  animate();
}

// Sidebar Functionality
function initializeSidebarFunctionality() {
  const menuToggle = document.getElementById('menuToggle');
  const closeSidebar = document.getElementById('closeSidebar');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('mobileMenuOverlay');
  
  function openSidebar() {
    sidebar.classList.add('sidebar-open');
    overlay.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
  
  function closeSidebarFunc() {
    sidebar.classList.remove('sidebar-open');
    overlay.classList.add('hidden');
    document.body.style.overflow = 'auto';
  }
  
  menuToggle.addEventListener('click', openSidebar);
  closeSidebar.addEventListener('click', closeSidebarFunc);
  overlay.addEventListener('click', closeSidebarFunc);
  
  // Close sidebar on escape key
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && sidebar.classList.contains('sidebar-open')) {
      closeSidebarFunc();
    }
  });
}

// Search Functionality
function initializeSearch() {
  const sidebarSearch = document.getElementById('sidebarSearch');
  const sidebarSearchResults = document.getElementById('sidebarSearchResults');
  let searchTimeout;
  
  sidebarSearch.addEventListener('input', function() {
    clearTimeout(searchTimeout);
    const query = this.value.trim();
    
    if (query.length < 2) {
      sidebarSearchResults.classList.add('hidden');
      return;
    }
    
    searchTimeout = setTimeout(() => {
      searchTools(query).then(results => {
        displaySidebarSearchResults(results);
      });
    }, 300);
  });
  
  function displaySidebarSearchResults(results) {
    if (results.length === 0) {
      sidebarSearchResults.innerHTML = '<div class="p-3 text-gray-400 text-center text-sm">No tools found</div>';
      sidebarSearchResults.classList.remove('hidden');
      return;
    }
    
    const html = results.map(result => `
      <a href="/${result.id}" class="block p-3 hover:bg-cyber-blue/10 transition-colors border-b border-gray-700 last:border-b-0">
        <div class="flex items-center space-x-2">
          <span class="text-lg">${result.icon}</span>
          <div>
            <h4 class="text-white font-medium text-sm">${result.name}</h4>
            <p class="text-gray-400 text-xs">${result.description.substring(0, 50)}...</p>
          </div>
        </div>
      </a>
    `).join('');
    
    sidebarSearchResults.innerHTML = html;
    sidebarSearchResults.classList.remove('hidden');
  }
  
  // Hide search results when clicking outside
  document.addEventListener('click', function(e) {
    if (!sidebarSearch.contains(e.target) && !sidebarSearchResults.contains(e.target)) {
      sidebarSearchResults.classList.add('hidden');
    }
  });
}

// Search Tools Function
async function searchTools(query) {
  try {
    const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    return await response.json();
  } catch (error) {
    console.error('Search error:', error);
    return [];
  }
}

// Category Toggle
function toggleCategory(categoryId) {
  const toolsDiv = document.getElementById(categoryId + '-tools');
  const arrow = document.getElementById(categoryId.substring(0, categoryId.indexOf('_') > -1 ? categoryId.indexOf('_') : categoryId.length) + '-arrow');
  
  if (toolsDiv.classList.contains('hidden')) {
    toolsDiv.classList.remove('hidden');
    if (arrow) arrow.style.transform = 'rotate(180deg)';
  } else {
    toolsDiv.classList.add('hidden');
    if (arrow) arrow.style.transform = 'rotate(0deg)';
  }
}

// Populate Featured Tools
function populateFeaturedTools() {
  const container = document.getElementById('featuredTools');
  if (!container) return;
  
  const html = featuredToolsData.map(tool => `
    <a href="/${tool.id}" class="tool-card rounded-2xl p-6 block group transform hover:scale-105 transition-all duration-300 fade-in">
      <div class="text-center">
        <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-r ${tool.gradient} flex items-center justify-center text-2xl">
          ${tool.icon}
        </div>
        <h3 class="text-xl font-bold text-white mb-2 group-hover:text-cyber-blue transition-colors">${tool.name}</h3>
        <p class="text-gray-400 text-sm font-inter leading-relaxed">${tool.description}</p>
      </div>
    </a>
  `).join('');
  
  container.innerHTML = html;
}

// Show All Tools
function showAllTools() {
  const allToolsSection = document.getElementById('allToolsSection');
  const featuredSection = document.getElementById('featuredTools').parentElement;
  
  if (allToolsSection.classList.contains('hidden')) {
    allToolsSection.classList.remove('hidden');
    featuredSection.style.display = 'none';
    
    // Smooth scroll to all tools section
    allToolsSection.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  } else {
    allToolsSection.classList.add('hidden');
    featuredSection.style.display = 'block';
  }
}

// Terminal Functionality
function initializeTerminal() {
  const terminalToggle = document.getElementById('terminalToggle');
  const terminalModal = document.getElementById('terminalModal');
  
  terminalToggle.addEventListener('click', function() {
    openTerminal();
  });
}

function openTerminal() {
  const modal = document.getElementById('terminalModal');
  const iframe = document.getElementById('terminalFrame');
  
  // Set up terminal iframe source
  iframe.src = 'data:text/html;charset=utf-8,' + encodeURIComponent(`
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { 
                margin: 0; 
                padding: 20px; 
                background: #000; 
                color: #00ff00; 
                font-family: 'Courier New', monospace; 
                font-size: 14px;
                overflow-y: auto;
            }
            .terminal-header {
                color: #00ff00;
                margin-bottom: 20px;
                border-bottom: 1px solid #333;
                padding-bottom: 10px;
            }
            .command-line {
                margin-bottom: 10px;
            }
            .prompt {
                color: #ff6b6b;
            }
            .output {
                color: #4ecdc4;
                margin-left: 20px;
                margin-bottom: 10px;
            }
            .warning {
                color: #ffeaa7;
            }
            .error {
                color: #fd79a8;
            }
        </style>
    </head>
    <body>
        <div class="terminal-header">
            <h2>🐧 Cloud Kali Linux Terminal (Beta)</h2>
            <p>Vaxyro Professional Cybersecurity Platform</p>
        </div>
        
        <div class="command-line">
            <span class="prompt">root@vaxyro:~#</span> <span>whoami</span>
        </div>
        <div class="output">root</div>
        
        <div class="command-line">
            <span class="prompt">root@vaxyro:~#</span> <span>uname -a</span>
        </div>
        <div class="output">Linux vaxyro-cloud 5.15.0-kali3-amd64 #1 SMP Debian 5.15.15-2kali1 (2022-01-31) x86_64 GNU/Linux</div>
        
        <div class="command-line">
            <span class="prompt">root@vaxyro:~#</span> <span>ls /usr/share/</span>
        </div>
        <div class="output">
            aircrack-ng  burpsuite  dirbuster  exploitdb  john  maltego<br>
            metasploit-framework  nmap  sqlmap  wireshark  wordlists
        </div>
        
        <div class="command-line">
            <span class="prompt">root@vaxyro:~#</span> <span>nmap --version</span>
        </div>
        <div class="output">
            Nmap version 7.93 ( https://nmap.org )<br>
            Platform: x86_64-pc-linux-gnu<br>
            Compiled with: liblua-5.3.6 openssl-3.0.7 libssh2-1.10.0
        </div>
        
        <div class="command-line">
            <span class="prompt">root@vaxyro:~#</span> <span>sqlmap --version</span>
        </div>
        <div class="output">
            sqlmap/1.7.2#stable (https://sqlmap.org)
        </div>
        
        <div class="warning">
            <br>⚠️  NOTICE: This is a demonstration terminal interface.<br>
            Full cloud terminal functionality coming soon in Vaxyro Pro!
        </div>
        
        <div class="command-line">
            <span class="prompt">root@vaxyro:~#</span> <span class="cursor">_</span>
        </div>
        
        <script>
            // Simple cursor blinking effect
            let cursor = document.querySelector('.cursor');
            setInterval(() => {
                cursor.style.opacity = cursor.style.opacity === '0' ? '1' : '0';
            }, 500);
        </script>
    </body>
    </html>
  `);
  
  modal.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeTerminal() {
  const modal = document.getElementById('terminalModal');
  modal.classList.add('hidden');
  document.body.style.overflow = 'auto';
}

// Utility Functions
function smoothScrollTo(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }
}

// Handle form submissions with better UX
document.addEventListener('submit', function(e) {
  if (e.target.tagName === 'FORM') {
    const submitBtn = e.target.querySelector('button[type="submit"]');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<span class="animate-spin">⚙️</span> Processing...';
    }
  }
});

// Add intersection observer for fade-in animations
const observerOptions = {
  threshold: 0.1,
  rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('fade-in');
    }
  });
}, observerOptions);

// Observe all tool cards for animation
setTimeout(() => {
  document.querySelectorAll('.tool-card').forEach(card => {
    observer.observe(card);
  });
}, 100);
