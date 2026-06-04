/**
 * Portable-Preferences-Portal: Universal Updater Engine
 * Automatically fetches public, non-PII configuration profiles
 * and maps them directly to active application instances.
 */

class PreferencesUpdaterEngine {
  constructor(configUrl) {
    this.configUrl = configUrl;
    this.preferences = null;
  }

  /**
   * Initializes the engine by fetching the remote JSON file
   */
  async init() {
    try {
      console.log(`[Preferences Engine] Syncing with profile: ${this.configUrl}`);
      const response = await fetch(this.configUrl, { cache: 'no-store' });
      
      if (!response.ok) {
        throw new Error(`HTTP network error! Status: ${response.status}`);
      }
      
      this.preferences = await response.json();
      console.log('[Preferences Engine] Remote sync successful.', this.preferences);
      
      // Execute all sub-engines sequentially
      this.applyAccessibility();
      this.applyUiAesthetics();
      this.applyLocalization();
      
      return true;
    } catch (error) {
      console.error('[Preferences Engine] Auto-sync failed:', error.message);
      return false;
    }
  }

  /**
   * 1. Accessibility Layer Mapping
   */
  applyAccessibility() {
    const acc = this.preferences?.accessibility;
    if (!acc) return;

    // Handle Animation & Motion Reduction
    if (acc.motion_reduction === true) {
      document.documentElement.style.setProperty('--engine-transition-speed', '0s');
      // Inject global rule to aggressively kill CSS animations if application supports it
      const style = document.createElement('style');
      style.id = 'pref-engine-motion-reduction';
      style.textContent = '* { animation-delay: 0s !important; animation-duration: 0s !important; transition-duration: 0s !important; }';
      document.head.appendChild(style);
      console.log(' - Motion reduction rules locked.');
    }

    // Handle High Contrast Mode
    if (acc.high_contrast === true) {
      document.documentElement.classList.add('forced-high-contrast');
      document.documentElement.setAttribute('aria-contrast', 'high');
    }

    // Handle Screen Reader Optimizations
    if (acc.screen_reader_optimized === true) {
      document.body.setAttribute('role', 'document');
      console.log(' - Semantic layout optimization enabled for readers.');
    }
  }

  /**
   * 2. UI/UX Aesthetics Layer Mapping
   */
  applyUiAesthetics() {
    const ui = this.preferences?.ui_aesthetics;
    if (!ui) return;

    // Handle Color Theme Injection
    if (ui.color_theme) {
      // Map 'system', 'dark', 'light', 'oled-black', 'sepia' directly to a data attribute
      document.documentElement.setAttribute('data-theme', ui.color_theme);
      console.log(` - Interface theme configured to: ${ui.color_theme}`);
    }

    // Handle Custom Brand Hex Accent
    if (ui.accent_color_hex) {
      document.documentElement.style.setProperty('--engine-accent-color', ui.accent_color_hex);
      console.log(` - UI accent variable set to: ${ui.accent_color_hex}`);
    }

    // Handle Font Multiplier Scale Factor
    if (ui.base_font_size_scale) {
      // Assuming a default root size of 16px, recalculate
      const calculatedPixels = 16 * parseFloat(ui.base_font_size_scale);
      document.documentElement.style.fontSize = `${calculatedPixels}px`;
      console.log(` - Root typography scaled to: ${calculatedPixels}px`);
    }

    // Handle Visual Structural Grid Density
    if (ui.layout_density) {
      document.documentElement.setAttribute('data-density', ui.layout_density);
    }
  }

  /**
   * 3. Localization Settings Mapping
   */
  applyLocalization() {
    const loc = this.preferences?.localization_environment;
    if (!loc) return;

    // Store local preferences in local memory storage so application code can read it anytime
    if (loc.temperature_unit) {
      localStorage.setItem('pref_app_temperature_unit', loc.temperature_unit);
    }
    if (loc.clock_format) {
      localStorage.setItem('pref_app_clock_format', loc.clock_format);
      console.log(` - Localization parameters stored in session state: ${loc.clock_format}`);
    }
  }
}

// Global invocation export or test trigger
// const configUrl = "https://githubusercontent.com";
// const engine = new PreferencesUpdaterEngine(configUrl);
// engine.init();
