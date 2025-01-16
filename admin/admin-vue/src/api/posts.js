import request from '@/utils/request'

// 文章列表接口
export function getPostList(params) {
  return request({
    url: '/api/posts/',
    method: 'get',
    params
  })
}

// 获取文章详情
export function getPostDetail(id) {
  return request({
    url: `/api/posts/${id}/`,
    method: 'get'
  })
}

// 创建文章
export function createPost(data) {
  return request({
    url: '/api/posts/',
    method: 'post',
    data
  })
}

// 更新文章
export function updatePost(id, data) {
  return request({
    url: `/api/posts/${id}/`,
    method: 'put',
    data
  })
}

// 删除文章
export function deletePost(id) {
  return request({
    url: `/api/posts/${id}/`,
    method: 'delete'
  })
}

// 切换文章状态
export function togglePostStatus(id) {
  return request({
    url: `/api/posts/${id}/toggle_status/`,
    method: 'post'
  })
}

// 上传文章图片
export function uploadPostImage(data) {
  return request({
    url: '/api/posts/upload-image/',
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data
  })
}

// 获取文章分类列表
export function getCategoryList() {
  return request({
    url: '/api/categories/',
    method: 'get'
  })
}

// 获取标签列表
export function getTagList() {
  return request({
    url: '/api/tags/',
    method: 'get'
  })
}

// 批量删除文章
export function batchDeletePosts(ids) {
  return request({
    url: '/api/posts/batch-delete/',
    method: 'post',
    data: { ids }
  })
} 