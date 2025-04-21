/**
 * 本地存储服务
 * 
 * 提供本地数据的存储和获取功能，支持缓存物品详情和其他应用数据
 * 包括缓存过期时间控制和数据版本管理
 */

const STORAGE_KEYS = {
  ITEMS_CACHE: 'findreve-items-cache',
  CACHE_VERSION: 'findreve-cache-version'
};

// 当前缓存版本号，当数据结构变更时修改此值使旧缓存失效
const CURRENT_CACHE_VERSION = '1.0';

// 缓存默认过期时间（24小时）
const DEFAULT_CACHE_EXPIRY = 24 * 60 * 60 * 1000;

class StorageService {
  constructor() {
    // 初始化时检查缓存版本，清除过期缓存
    this.initializeCache();
  }

  /**
   * 初始化缓存
   * 
   * 检查缓存版本，如果版本不匹配则清除所有缓存
   */
  initializeCache() {
    try {
      const cachedVersion = localStorage.getItem(STORAGE_KEYS.CACHE_VERSION);
      
      // 如果版本号不匹配，清除所有缓存
      if (cachedVersion !== CURRENT_CACHE_VERSION) {
        console.log('Cache version mismatch, clearing cache...');
        this.clearAllCache();
        localStorage.setItem(STORAGE_KEYS.CACHE_VERSION, CURRENT_CACHE_VERSION);
      }
    } catch (error) {
      console.error('Error initializing cache:', error);
      // 出错时尝试清除缓存
      this.clearAllCache();
    }
  }

  /**
   * 保存物品数据到本地缓存
   * 
   * @param {string} key - 物品唯一标识
   * @param {Object} itemData - 物品详情数据
   * @param {number} expiryTime - 缓存过期时间(毫秒)，默认24小时
   */
  saveItemToCache(key, itemData, expiryTime = DEFAULT_CACHE_EXPIRY) {
    try {
      // 获取现有缓存
      const itemsCache = this.getAllCachedItems() || {};
      
      // 更新缓存，添加时间戳
      itemsCache[key] = {
        data: itemData,
        timestamp: Date.now(),
        expiry: expiryTime
      };
      
      // 保存回本地存储
      localStorage.setItem(STORAGE_KEYS.ITEMS_CACHE, JSON.stringify(itemsCache));
      
      console.log(`Item cached: ${key}`);
    } catch (error) {
      console.error('Error saving item to cache:', error);
    }
  }

  /**
   * 从缓存获取物品数据
   * 
   * @param {string} key - 物品唯一标识
   * @returns {Object|null} 缓存的物品数据，如果不存在或已过期则返回null
   */
  getItemFromCache(key) {
    try {
      const itemsCache = this.getAllCachedItems() || {};
      const cachedItem = itemsCache[key];
      
      // 检查是否存在缓存
      if (!cachedItem) {
        return null;
      }
      
      // 检查缓存是否过期
      const now = Date.now();
      if (now - cachedItem.timestamp > cachedItem.expiry) {
        console.log(`Cache expired for item: ${key}`);
        this.removeItemFromCache(key);
        return null;
      }
      
      console.log(`Cache hit for item: ${key}`);
      return cachedItem.data;
    } catch (error) {
      console.error('Error retrieving item from cache:', error);
      return null;
    }
  }

  /**
   * 获取缓存项的时间戳
   * 
   * @param {string} key - 缓存项的唯一标识
   * @returns {number|null} 缓存项的时间戳，如果不存在则返回null
   */
  getCacheTimestamp(key) {
    try {
      const itemsCache = this.getAllCachedItems() || {};
      const cachedItem = itemsCache[key];
      
      if (cachedItem && cachedItem.timestamp) {
        return cachedItem.timestamp;
      }
      return null;
    } catch (error) {
      console.error('Error getting cache timestamp:', error);
      return null;
    }
  }

  /**
   * 从缓存中移除物品数据
   * 
   * @param {string} key - 物品唯一标识
   */
  removeItemFromCache(key) {
    try {
      const itemsCache = this.getAllCachedItems() || {};
      
      if (itemsCache[key]) {
        delete itemsCache[key];
        localStorage.setItem(STORAGE_KEYS.ITEMS_CACHE, JSON.stringify(itemsCache));
        console.log(`Removed item from cache: ${key}`);
      }
    } catch (error) {
      console.error('Error removing item from cache:', error);
    }
  }

  /**
   * 获取所有缓存的物品数据
   * 
   * @returns {Object|null} 包含所有缓存物品的对象
   */
  getAllCachedItems() {
    try {
      const cachedData = localStorage.getItem(STORAGE_KEYS.ITEMS_CACHE);
      return cachedData ? JSON.parse(cachedData) : {};
    } catch (error) {
      console.error('Error getting all cached items:', error);
      return {};
    }
  }

  /**
   * 清理过期的缓存项目
   * 
   * 遍历所有缓存项目并移除已过期的条目
   */
  cleanExpiredCache() {
    try {
      const now = Date.now();
      const itemsCache = this.getAllCachedItems() || {};
      let hasExpired = false;
      
      // 检查每个缓存项是否过期
      Object.keys(itemsCache).forEach(key => {
        const item = itemsCache[key];
        if (now - item.timestamp > item.expiry) {
          delete itemsCache[key];
          hasExpired = true;
          console.log(`Expired cache removed: ${key}`);
        }
      });
      
      // 如果有过期项，更新缓存
      if (hasExpired) {
        localStorage.setItem(STORAGE_KEYS.ITEMS_CACHE, JSON.stringify(itemsCache));
      }
    } catch (error) {
      console.error('Error cleaning expired cache:', error);
    }
  }

  /**
   * 清除所有缓存数据
   */
  clearAllCache() {
    try {
      localStorage.removeItem(STORAGE_KEYS.ITEMS_CACHE);
      console.log('All cache cleared');
    } catch (error) {
      console.error('Error clearing cache:', error);
    }
  }
}

export default new StorageService();
