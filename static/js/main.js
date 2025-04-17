async function login(username, password) {
    const url = '/api/token';
    const data = new URLSearchParams();
    data.append('username', username);
    data.append('password', password);

try {
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: data,
    });

    if (!response.ok) {
        throw new Error('登录失败: ' + response.statusText);
    }

    const result = await response.json();

    // 处理登录成功后的数据，返回access_token
    localStorage.setItem('access_token', result.access_token);

    return {'status': 'success'};

} catch (error) {
    return {'status': 'failed', 'detail': error.message};
}
}

async function is_login() {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
        return false;
    }
    try {
        const response = await fetch('/api/admin', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            }
        })
        
        if (!response.ok) {
            return false;
        }
        
        return true;
    }
    catch (error) {
        return false;
    }
}

function logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
}

async function getItem(id) {
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        return {'status': 'failed', 'detail': 'Access token not found'};
    }

    const url = `/api/admin/items?id=${encodeURIComponent(id)}`;

    try {
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('请求失败: ' + response.statusText);
        }

        const data = await response.json();
        return {'status': 'success', 'data': data};

    } catch (error) {
        console.error('Get item error:', error);
        return {'status': 'failed', 'detail': error.message};
    }
}

async function getItems() {
    const accessToken = localStorage.getItem('access_token');
    
    if (!accessToken) {
        return {'status': 'failed', 'detail': 'Access token not found'};
    }

    const url = '/api/admin/items';

    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
            },
        });

        if (!response.ok) {
            throw new Error('请求失败: ' + response.statusText);
        }

        const data = await response.json();

        return {'status': 'success', 'data': data};

    } catch (error) {
        return {'status': 'failed', 'detail': error.message};
    }
}

async function addItems(key, name, icon, phone) {
    const accessToken = localStorage.getItem('access_token');
    
    // 构建带参数的URL
    const url = `/api/admin/items?key=${encodeURIComponent(key)}&name=${encodeURIComponent(name)}&icon=${encodeURIComponent(icon)}&phone=${encodeURIComponent(phone)}`;
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'accept': 'application/json'
            },
            body: ''
        });

        if (!response.ok) {
            throw new Error('请求失败: ' + response.statusText);
        }

        const result = await response.json();
        return {'status': 'success', 'data': result};

    } catch (error) {
        console.error('Add items error:', error);
        return {'status': 'failed', 'detail': error.message};
    }
}

async function updateItems(id, key, name, icon, phone, status, context) {
    const accessToken = localStorage.getItem('access_token');
    
    // 通过URL查询参数发送数据
    let url = `/api/admin/items?id=${encodeURIComponent(id)}&key=${encodeURIComponent(key)}&name=${encodeURIComponent(name)}&icon=${encodeURIComponent(icon)}&phone=${encodeURIComponent(phone)}`;
    
    // 添加状态参数
    if (status) {
        url += `&status=${encodeURIComponent(status)}`;
    }
    
    // 只在有context且status为lost时添加context参数
    if (context && status === 'lost') {
        url += `&context=${encodeURIComponent(context)}`;
    }
    
    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'accept': 'application/json'
            },
            body: ''
        });

        if (!response.ok) {
            throw new Error('请求失败: ' + response.statusText);
        }

        const result = await response.json();
        return {'status': 'success', 'data': result};

    } catch (error) {
        console.error('Update items error:', error);
        return {'status': 'failed', 'detail': error.message};
    }
}

async function deleteItem(id) {
    const accessToken = localStorage.getItem('access_token');
    
    // 构建URL，带上物品id参数
    const url = `/api/admin/items?id=${encodeURIComponent(id)}`;
    
    try {
        const response = await fetch(url, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error('请求失败: ' + response.statusText);
        }

        const result = await response.json();
        return {'status': 'success', 'data': result};

    } catch (error) {
        console.error('Delete item error:', error);
        return {'status': 'failed', 'detail': error.message};
    }
}

async function get_about() {
    try {
        const response = await fetch('/static/readme.md', {
            method: 'GET',
            cache: 'no-cache' // 防止缓存问题
        });

        if (!response.ok) {
            console.error('获取readme失败:', response.status);
            return '无法加载内容: ' + response.statusText;
        }

        const data = await response.text();
        return data;

    } catch (error) {
        console.error('获取readme错误:', error);
        return '加载错误: ' + error.message;
    }
}

async function getObject(key) {
    try {
        const response = await fetch(`/api/object/${encodeURIComponent(key)}`, {
            method: 'GET',
            headers: {
                'accept': 'application/json'
            },
        });

        if (!response.ok) {
            throw new Error('请求失败: ' + response.statusText);
        }

        const result = await response.json();
        return {'status': 'success', 'data': result.data};

    } catch (error) {
        console.error('Get object error:', error);
        return {'status': 'failed', 'detail': error.message};
    }
}