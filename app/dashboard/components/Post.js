import React from 'react'
import { Link } from 'react-router-dom'
import { inject, observer } from 'mobx-react'

import moment from 'moment'

import { MainContainer, Section} from './Layout'


function DraftPreview(post) {
  return (
    <div key={post.id} className="post-item two-column">
      <div className="two-column-main">
        <Link className="post-item-link" to={`/editor/${post.id}`}>
          <strong>{post.title}</strong>
        </Link>
        <div className="post-item-info">
          {post.metas.map((meta) =>
            <span key={meta.slug}>{meta.name}</span>
          )}
        </div>
      </div>
    </div>
  )
}


function PostPreview(post) {
  return (
    <div key={post.id} className="post-item two-column">
      <div className="two-column-main">
        <Link className="post-item-link" to={`/editor/${post.id}`}>
          <strong>{post.title}</strong>
          <span>{post.headline}</span>
        </Link>
        <div className="post-item-info">
          {post.metas.map((meta) =>
            <span key={meta.slug}>{meta.name}</span>
          )}
          <a href={post.url}>{moment(post.created).format('ll')}</a>
        </div>
      </div>
      <div className="two-column-action">
        <div className="post-item-views">
          <strong>{post.views}</strong> views
        </div>
      </div>
    </div>
  )
}


function PostList(props) {
  return (
    <div className="content">
      {props.data.map((post) =>
        props.component(post)
      )}
    </div>
  )
}


@inject('postStore', 'asideStore')
@observer
class Post extends React.Component {

  componentDidMount() {
    this.props.postStore.fetch()
    this.props.asideStore.show()
  }

  render() {
    const newPostButton = (
        <Link to="/editor">
          <button type="button" className="btn btn-primary">
            <span>New Post</span>
          </button>
        </Link>
      )
    return (
      <MainContainer>
        <Section title="Drafts" action={newPostButton}>
          <PostList component={DraftPreview} data={[]} />
        </Section>
        <Section title="Published">
          <PostList component={PostPreview} data={this.props.postStore.posts} />
        </Section>
      </MainContainer>
    )
  }

}

export default Post