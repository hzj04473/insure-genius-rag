/**
 * 모달 유틸리티 함수들
 * 보험 플랫폼에서 사용하는 공통 모달 기능
 */

class ModalUtils {
  /**
   * 기본 모달 생성
   * @param {string} title - 모달 제목
   * @param {string} content - 모달 내용 (HTML)
   * @param {Object} options - 모달 옵션
   */
  static createModal(title, content, options = {}) {
    const defaults = {
      size: 'medium', // small, medium, large
      closable: true,
      backdrop: true,
      keyboard: true,
      buttons: [],
    };

    const config = { ...defaults, ...options };

    // 기존 모달 제거
    const existingModal = document.getElementById('dynamic-modal');
    if (existingModal) {
      existingModal.remove();
    }

    // 모달 HTML 생성
    const modalHTML = `
            <div class="modal fade" id="dynamic-modal" tabindex="-1" aria-labelledby="modalTitle" aria-hidden="true">
                <div class="modal-dialog modal-${config.size}">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="modalTitle">${title}</h5>
                            ${
                              config.closable
                                ? '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'
                                : ''
                            }
                        </div>
                        <div class="modal-body">
                            ${content}
                        </div>
                        ${
                          config.buttons.length > 0
                            ? `
                        <div class="modal-footer">
                            ${config.buttons
                              .map(
                                (btn) => `
                                <button type="button" class="btn btn-${btn.type || 'secondary'}" 
                                        onclick="${btn.onclick || ''}" 
                                        ${btn.dismiss ? 'data-bs-dismiss="modal"' : ''}>
                                    ${btn.text}
                                </button>
                            `
                              )
                              .join('')}
                        </div>
                        `
                            : ''
                        }
                    </div>
                </div>
            </div>
        `;

    // DOM에 추가
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // 모달 표시
    const modal = new bootstrap.Modal(document.getElementById('dynamic-modal'), {
      backdrop: config.backdrop,
      keyboard: config.keyboard,
    });

    modal.show();

    return modal;
  }

  /**
   * 확인 모달
   * @param {string} message - 확인 메시지
   * @param {Function} onConfirm - 확인 시 실행할 함수
   */
  static confirm(message, onConfirm) {
    return this.createModal('확인', message, {
      buttons: [
        {
          text: '취소',
          type: 'secondary',
          dismiss: true,
        },
        {
          text: '확인',
          type: 'primary',
          onclick: `(${onConfirm.toString()})(); bootstrap.Modal.getInstance(document.getElementById('dynamic-modal')).hide();`,
        },
      ],
    });
  }

  /**
   * 알림 모달
   * @param {string} message - 알림 메시지
   * @param {string} type - 알림 타입 (info, success, warning, error)
   */
  static alert(message, type = 'info') {
    const typeConfig = {
      info: { title: '알림', icon: 'ℹ️' },
      success: { title: '성공', icon: '✅' },
      warning: { title: '경고', icon: '⚠️' },
      error: { title: '오류', icon: '❌' },
    };

    const config = typeConfig[type] || typeConfig.info;

    return this.createModal(config.title, `${config.icon} ${message}`, {
      buttons: [
        {
          text: '확인',
          type: type === 'error' ? 'danger' : 'primary',
          dismiss: true,
        },
      ],
    });
  }

  /**
   * 로딩 모달
   * @param {string} message - 로딩 메시지
   */
  static showLoading(message = '처리 중...') {
    const loadingHTML = `
            <div class="text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3">${message}</p>
            </div>
        `;

    return this.createModal('', loadingHTML, {
      closable: false,
      backdrop: 'static',
      keyboard: false,
    });
  }

  /**
   * 로딩 모달 숨기기
   */
  static hideLoading() {
    const modal = document.getElementById('dynamic-modal');
    if (modal) {
      const modalInstance = bootstrap.Modal.getInstance(modal);
      if (modalInstance) {
        modalInstance.hide();
      }
    }
  }
}

// 전역에서 사용할 수 있도록 window 객체에 추가
window.ModalUtils = ModalUtils;

// jQuery 스타일 단축 함수들
window.showModal = (title, content, options) => ModalUtils.createModal(title, content, options);
window.confirmModal = (message, onConfirm) => ModalUtils.confirm(message, onConfirm);
window.alertModal = (message, type) => ModalUtils.alert(message, type);
window.showLoading = (message) => ModalUtils.showLoading(message);
window.hideLoading = () => ModalUtils.hideLoading();
