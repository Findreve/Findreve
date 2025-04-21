/**
 * API 服务
 * 
 * 提供统一的 HTTP 请求处理，包括认证令牌管理、错误处理等功能。
 * 自动处理令牌过期情况，在令牌失效时重定向到登录页面。
 * 集成了本地缓存功能，支持优先使用缓存数据。
 */

import router from '@/router';
import storageService from './storage_service';

class ApiService {
  /**
   * 发送 HTTP 请求
   * 
   * @param {string} url - 请求地址
   * @param {Object} options - 请求选项
   * @returns {Promise<Object>} 响应数据
   */
  async request(url, options = {}) {
    // 默认请求头
    const headers = {
      'accept': 'application/json',
      ...options.headers
    };

    // 添加认证令牌
    const token = localStorage.getItem('user-token');
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      });

      // 处理认证错误
      if (response.status === 401) {
        console.log('认证失败，可能是令牌已过期');
        // 清除过期的令牌
        localStorage.removeItem('user-token');
        
        // 保存当前路径，用于登录后跳转回来
        const currentPath = router.currentRoute.value.fullPath;
        if (currentPath !== '/login') {
          // 跳转到登录页面，带上重定向参数
          router.push({
            path: '/login',
            query: { redirect: currentPath, expired: 'true' }
          });
          
          // 抛出错误，中断后续处理
          throw new Error('认证已过期，请重新登录');
        }
      }

      // 处理其他错误
      if (!response.ok) {
        // 尝试解析错误信息
        let errorMessage;
        try {
          const errorData = await response.json();
          errorMessage = errorData.msg || errorData.detail || `请求失败: ${response.status}`;
        } catch (e) {
          errorMessage = `请求失败: ${response.status} ${response.statusText}`;
        }
        throw new Error(errorMessage);
      }

      return await response.json();
    } catch (error) {
      console.error('API 请求错误:', error);
      throw error;
    }
  }

  /**
   * GET 请求
   * 
   * @param {string} url - 请求地址
   * @param {Object} options - 请求选项
   * @returns {Promise<Object>} 响应数据
   */
  get(url, options = {}) {
    return this.request(url, {
      method: 'GET',
      ...options
    });
  }

  /**
   * POST 请求
   * 
   * @param {string} url - 请求地址
   * @param {Object|FormData|string} data - 请求数据
   * @param {Object} options - 请求选项
   * @returns {Promise<Object>} 响应数据
   */
  post(url, data, options = {}) {
    const requestOptions = {
      method: 'POST',
      ...options
    };

    // 根据数据类型设置请求体和内容类型
    if (data) {
      if (data instanceof FormData) {
        requestOptions.body = data;
      } else if (typeof data === 'string') {
        requestOptions.body = data;
      } else {
        requestOptions.body = JSON.stringify(data);
        requestOptions.headers = {
          'Content-Type': 'application/json',
          ...options.headers
        };
      }
    }

    return this.request(url, requestOptions);
  }

  /**
   * PATCH 请求
   * 
   * @param {string} url - 请求地址
   * @param {Object|FormData|string} data - 请求数据
   * @param {Object} options - 请求选项
   * @returns {Promise<Object>} 响应数据
   */
  patch(url, data, options = {}) {
    const requestOptions = {
      method: 'PATCH',
      ...options
    };

    // 处理请求体
    if (data) {
      if (data instanceof FormData || typeof data === 'string') {
        requestOptions.body = data;
      } else {
        requestOptions.body = JSON.stringify(data);
        requestOptions.headers = {
          'Content-Type': 'application/json',
          ...options.headers
        };
      }
    } else {
      requestOptions.body = '';
    }

    return this.request(url, requestOptions);
  }

  /**
   * DELETE 请求
   * 
   * @param {string} url - 请求地址
   * @param {Object} options - 请求选项
   * @returns {Promise<Object>} 响应数据
   */
  delete(url, options = {}) {
    return this.request(url, {
      method: 'DELETE',
      ...options
    });
  }

  /**
   * 提交表单数据
   * 
   * @param {string} url - 请求地址
   * @param {Object} formData - 表单数据对象
   * @param {Object} options - 请求选项
   * @returns {Promise<Object>} 响应数据
   */
  submitForm(url, formData, options = {}) {
    const urlSearchParams = new URLSearchParams();
    
    // 将对象转换为 URLSearchParams
    Object.keys(formData).forEach(key => {
      if (formData[key] !== undefined && formData[key] !== null) {
        urlSearchParams.append(key, formData[key]);
      }
    });

    return this.post(url, urlSearchParams.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      ...options
    });
  }

  /**
   * 登录请求
   * 
   * @param {string} username - 用户名
   * @param {string} password - 密码
   * @returns {Promise<Object>} 登录结果
   */
  async login(username, password) {
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);
      formData.append('grant_type', 'password');

      const response = await fetch('/api/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'accept': 'application/json'
        },
        body: formData
      });

      if (!response.ok) {
        let errorMessage = '登录失败';
        if (response.status === 401) {
          errorMessage = '账号或密码错误';
        } else {
          try {
            const errorData = await response.json();
            errorMessage = errorData.detail || '登录失败';
          } catch (e) {
            console.error('解析错误响应失败:', e);
          }
        }
        throw new Error(errorMessage);
      }

      const data = await response.json();
      localStorage.setItem('user-token', data.access_token);
      
      return { success: true, data };
    } catch (error) {
      console.error('登录错误:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * 验证当前令牌是否有效
   * 
   * 通过调用 /api/admin/ 接口验证当前令牌的有效性
   * 
   * @returns {Promise<boolean>} 令牌是否有效
   */
  async validateToken() {
    try {
      // 检查是否有令牌
      const token = localStorage.getItem('user-token');
      if (!token) {
        console.log('没有找到认证令牌');
        return false;
      }
      
      // 调用验证接口
      const response = await this.get('/api/admin/');
      return response === true;
    } catch (error) {
      console.log('令牌验证失败:', error);
      return false;
    }
  }

  /**
   * 获取物品详情
   * 
   * 根据物品标识码获取物品信息，支持缓存机制
   * 
   * @param {string} key - 物品标识码
   * @param {boolean} useCache - 是否优先使用缓存数据
   * @returns {Promise<Object>} 物品详情
   */
  async getObject(key, useCache = true) {
    try {
      // 1. 如果允许使用缓存，先检查是否有缓存数据
      if (useCache) {
        const cachedItem = storageService.getItemFromCache(key);
        if (cachedItem) {
          console.log('Using cached item data:', key);
          return cachedItem;
        }
      }
      
      // 2. 没有缓存或不使用缓存，从API获取数据
      const data = await this.get(`/api/object/${encodeURIComponent(key)}`);
      
      if (data.code === 0) {
        // 3. 获取数据成功后，保存到缓存
        storageService.saveItemToCache(key, data.data);
        return data.data;
      } else {
        throw new Error(data.msg || '获取物品信息失败');
      }
    } catch (error) {
      console.error('获取物品错误:', error);
      throw error;
    }
  }

  /**
   * 清除API结果缓存
   * 可用于强制刷新数据或在用户登出时清除敏感信息
   */
  clearCache() {
    storageService.clearAllCache();
  }
}

export default new ApiService();
