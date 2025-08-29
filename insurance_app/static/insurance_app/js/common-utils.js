/**
 * 공통 JavaScript 유틸리티 함수들
 * 모든 앱에서 사용할 수 있는 재사용 가능한 함수들
 */

// DOM 유틸리티
const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));

// 공통 UI 유틸리티
const UIUtils = {
  // 토스트 메시지 표시
  showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `alert-unified ${type} fade-in-unified`;
    toast.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      z-index: 9999;
      min-width: 300px;
      box-shadow: var(--shadow-lg);
    `;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },

  // 로딩 스피너 표시/숨김
  showLoading(element) {
    const spinner = document.createElement('span');
    spinner.className = 'spinner-unified';
    spinner.style.marginLeft = '8px';
    element.appendChild(spinner);
    element.disabled = true;
    return spinner;
  },

  hideLoading(element, spinner) {
    if (spinner && spinner.parentNode) {
      spinner.remove();
    }
    element.disabled = false;
  },

  // 모달 생성
  createModal(title, content, options = {}) {
    const modal = document.createElement('div');
    modal.className = 'modal-unified fade-in-unified';

    modal.innerHTML = `
      <div class="modal-content-unified slide-up-unified">
        <div class="modal-header-unified">
          <h3 style="margin: 0; color: var(--text-primary);">${title}</h3>
          <button class="btn-unified" onclick="this.closest('.modal-unified').remove()">
            ✕
          </button>
        </div>
        <div class="modal-body-unified">
          ${content}
        </div>
      </div>
    `;

    // 배경 클릭시 닫기
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.remove();
      }
    });

    document.body.appendChild(modal);
    return modal;
  },

  // 확인 다이얼로그
  confirm(message, onConfirm, onCancel) {
    const content = `
      <p style="margin-bottom: 20px; color: var(--text-secondary);">${message}</p>
      <div style="display: flex; gap: 12px; justify-content: flex-end;">
        <button class="btn-unified" onclick="this.closest('.modal-unified').remove(); (${onCancel || (() => {})})()">
          취소
        </button>
        <button class="btn-unified primary" onclick="this.closest('.modal-unified').remove(); (${onConfirm})()">
          확인
        </button>
      </div>
    `;

    return this.createModal('확인', content);
  },
};

// 폼 유틸리티
const FormUtils = {
  // 폼 데이터를 객체로 변환
  serializeForm(form) {
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {
      if (data[key]) {
        if (Array.isArray(data[key])) {
          data[key].push(value);
        } else {
          data[key] = [data[key], value];
        }
      } else {
        data[key] = value;
      }
    }
    return data;
  },

  // 입력 필드 유효성 검사
  validateField(field, rules) {
    const value = field.value.trim();
    const errors = [];

    if (rules.required && !value) {
      errors.push('필수 입력 항목입니다.');
    }

    if (rules.minLength && value.length < rules.minLength) {
      errors.push(`최소 ${rules.minLength}자 이상 입력해주세요.`);
    }

    if (rules.pattern && !rules.pattern.test(value)) {
      errors.push(rules.message || '올바른 형식으로 입력해주세요.');
    }

    // 에러 표시
    const errorElement = field.parentNode.querySelector('.field-error');
    if (errorElement) {
      errorElement.remove();
    }

    if (errors.length > 0) {
      field.classList.add('invalid');
      const errorDiv = document.createElement('div');
      errorDiv.className = 'field-error';
      errorDiv.style.cssText = 'color: var(--danger-color); font-size: 13px; margin-top: 4px;';
      errorDiv.textContent = errors[0];
      field.parentNode.appendChild(errorDiv);
      return false;
    } else {
      field.classList.remove('invalid');
      return true;
    }
  },
};

// API 유틸리티
const APIUtils = {
  // CSRF 토큰 가져오기
  getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split('=');
      if (name === 'csrftoken') {
        return decodeURIComponent(value);
      }
    }
    return null;
  },

  // 공통 fetch 래퍼
  async request(url, options = {}) {
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.getCSRFToken(),
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, { ...defaultOptions, ...options });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      } else {
        return await response.text();
      }
    } catch (error) {
      console.error('API 요청 실패:', error);
      UIUtils.showToast('서버 요청 중 오류가 발생했습니다.', 'error');
      throw error;
    }
  },
};

// 칩/태그 컨트롤러
const ChipController = {
  init(container, options = {}) {
    const { multiple = true, onSelect = null } = options;
    const selected = new Set();

    // 초기 선택된 항목들 수집
    container.querySelectorAll('.chip-unified.selected').forEach((chip) => {
      const value = chip.dataset.value;
      if (value) selected.add(value);
    });

    container.addEventListener('click', (e) => {
      const chip = e.target.closest('.chip-unified');
      if (!chip) return;

      const value = chip.dataset.value;
      if (!value) return;

      if (multiple) {
        chip.classList.toggle('selected');
        if (chip.classList.contains('selected')) {
          selected.add(value);
        } else {
          selected.delete(value);
        }
      } else {
        // 단일 선택
        container.querySelectorAll('.chip-unified').forEach((c) => c.classList.remove('selected'));
        chip.classList.add('selected');
        selected.clear();
        selected.add(value);
      }

      if (onSelect) {
        onSelect(Array.from(selected), value);
      }
    });

    return {
      getSelected: () => Array.from(selected),
      setSelected: (values) => {
        selected.clear();
        container.querySelectorAll('.chip-unified').forEach((chip) => {
          const value = chip.dataset.value;
          if (values.includes(value)) {
            chip.classList.add('selected');
            selected.add(value);
          } else {
            chip.classList.remove('selected');
          }
        });
      },
    };
  },
};

// 전역으로 노출
window.UIUtils = UIUtils;
window.FormUtils = FormUtils;
window.APIUtils = APIUtils;
window.ChipController = ChipController;
window.$ = $;
window.$$ = $$;
