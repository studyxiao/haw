## 文件上传

目前仅支持图片上传至服务器并 s 录在数据库 file 表中

### 使用

```python
files = request.file
res = []
for file in files:
	item = Uploader(file).uplode()
  res.append(item)
 return jsonify(res)
```

### 返回

```json
{
  "key": "文件名称",
  "id": "数据库中id",
  "url": "路径"
}
```

### 内置接口

**上传**

接口：`/api/image`

字段： `image`

**展示、下载**

接口：`/api/image/<filename>`

参数：filename 为返回的 url 字段或数据表 file 中的 path 字段
