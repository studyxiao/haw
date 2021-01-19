## 数据库增改删查操作

|   方法   |                              方法名                               |                                                                                                                            参数                                                                                                                            |  说明  |
| :------: | :---------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :----: |
|   新增   |                         create(\*\*data)                          |                                                                                                                          字段=值                                                                                                                           | 类方法 |
|   修改   |                 update(id, \*condition, \*\*data)                 |                                                                                 id 需要修改的数据 id<br />condition 额外过滤条件，如文章是否属于用户<br />data 修改字段=值                                                                                 | 类方法 |
|   删除   |                   delete(id, hard, \*condition)                   |                                                                     id 删除数据的 id<br />hard 是否应删除，默认软删除（设置删除时间，但数据还还在数据库）<br />condition 额外过滤条件                                                                      | 类方法 |
| 获取一个 |                     get(\*query, \*\*kwargs)                      |                                                                                      query: 查询条件，e.g. Article.publish==1<br />kwargs: 查询条件，e.g. title='tit'                                                                                      | 类方法 |
| 获得多个 |              find(query=None, by=None, \*\*kwargs):               |                                                                                    query: ['Article.status==1']<br />by: [Article.sort.desc]<br />kwargs: title='hello'                                                                                    | 类方法 |
|   分页   | find_by_page(query, by, start, count, \_query=None, fields=None): | query: 查询条件，[Article.status==1]<br/> by: 排序，[Article.created]<br/> start: 起始位置<br/> count: 个数<br/> \_query: 查询集 cls.query.filter()，设置后会在此基础上进行查询<br/> fields: 返回前端字段，['id', 'title', 'content']，默认 model.\_fields | 类方法 |

## 返回数据过滤

- hide_fields(*args) 隐藏某个字段
- add_fields(*kwargs) 增加某个自定义字段