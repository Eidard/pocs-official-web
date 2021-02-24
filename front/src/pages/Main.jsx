import React, { useEffect, useState } from 'react';
import {Link, withRouter}             from 'react-router-dom';
import styled                         from 'styled-components';

import Backdrop                       from '../components/Backdrop';

import { getPosts }                   from '../api/Api';

import { formatDate }                 from '../utils/Format';

const Wrapper = styled.main`
  margin:           0px;
  background-color: #eee;
  height:           100%;
  text-align:       center;
`;

const Header = styled.header`
  display:          flex;
  flex-direction:   column;
  height:           300px;
  margin-bottom:    10px;
  background-color: darkblue;
`;

const HeaderContent = styled.div`
  text-align:       left;
  font-size:        24px;
  color:            white;
  max-width:        1400px;
  margin-right:     auto;
  padding:          50px;
`

const LogoText = styled.div`
  display:          inline-block;
  margin:           15px;
  margin-right:     20px;
  line-height:      30px;
  vertical-align:   middle;
  font-size:        28px;
  font-weight:      bold;
  color:            white;
`

const NavigationBarRoot = styled.nav`
  display:          flex;
  align-items:      center;
`

const NavigationBarList = styled.ul`
  display:          flex;
  align-items:      center;
  list-style-type:  none;
  margin-left:      auto;
  overflow:         hidden;
`

const NavigationBarItem = styled.li`
  font-size:        14px;
  line-height:      30px;
  margin-left:      16px;
  margin-right:     16px;
  display:          inline-block;
  vertical-align:   middle;
  text-decoration:  none;
  color:            white;
`

const NavigationBarImageItem = styled.img`
  width:            20px;
  height:           20px;
  margin-left:      16px;
  margin-right:     16px;
  filter:           invert(1);
  vertical-align:   middle;
`

const HeaderContentTitle = styled.p`
  font-size:        40px;
  font-weight:      bold;
  margin-bottom:    10px;
`

const HeaderContentText = styled.p`
  font-size:        16px;
  color:            lightgray;
`

const Section = styled.section`
  display:          flex;
  flex-flow:        row wrap;
  align-content:    center;
  align-items:      center;
  margin:           auto;
  text-align:       center;
`

const Article = styled.article`
  display:          flex;
  justify-content:  center;
  flex:             0 1 1200px;
  margin:           10px auto;
  padding:          20px;
  width:            1200px;
  display:          inline-block;
  background-color: white;
  text-align:       left;
`

const ArticleTitle = styled.h1`
  font-size:        16px;
  margin-bottom:    20px;
`

const ArticleRowWrapper = styled.div`
  display:          flex;
  margin-bottom:    5px;
`

const ArticleRowTitle = styled.span`
  margin:           5px 5px 0px 0px;
  font-size:        14px;
`

const ArticleRowText = styled.span`
  margin:           5px 5px 0px 0px;
  font-size:        14px;
`

const ArticleRowDate = styled.span`
  margin-left:      auto;
  font-size:        14px;
`

const NoticeBarWrapper = styled.div`
  display:          flex;
  justify-content:  center;
  margin:           10px auto;
  padding:          20px;
  width:            1200px;
  text-align:       left;
  vertical-align:   center;
  background-color: white;
`

const NoticeBarTitle = styled.span`
  font-weight:      bold;
  margin-right:     10px;
  font-size:        16px;
  line-height:      20px;
`

const NoticeBarText = styled.span`
  font-size:        14px;
  line-height:      20px;
`

const NoticeBarDate = styled.span`
  margin-left:      auto;
  font-size:        14px;
  line-height:      20px;
`

const Logo = (props) => {
  return <Link to="/">
    <LogoText>{ props.text }</LogoText>
  </Link>
}

const NavigationBarButton = (props) => {
  return <Link to={ props.to }>
    <NavigationBarItem>{ props.text }</NavigationBarItem>
  </Link>
}

const AccountButton = () => {
  return <Link to="/login">
    <NavigationBarImageItem src="/images/main/account.png"/>
  </Link>
}

const SearchButton = () => {
  return <NavigationBarImageItem src="/images/main/search.png"/>
}

const ArticleTitleButton = (props) => {
  return(
    <Link to={ props.to } style={{ textDecoration: 'none', color: 'black' }}>
      <ArticleTitle>{ props.text }</ArticleTitle>
    </Link>
  );
}

const ArticleRow = (props) => {
  return(
    <Link to={ props.to } style={{ textDecoration: 'none', color: 'black' }}>
      <ArticleRowWrapper>
        <ArticleRowTitle>{ props.title }</ArticleRowTitle>
        <ArticleRowDate>{ props.date }</ArticleRowDate>
      </ArticleRowWrapper>
    </Link>
  );
}

const NoticeBar = (props) => {
  return(
  <NoticeBarWrapper>
    <NoticeBarTitle>공지사항</NoticeBarTitle>
    <NoticeBarText>{ props.text }</NoticeBarText>
    <NoticeBarDate>{ props.date }</NoticeBarDate>
  </NoticeBarWrapper>
  );
}

export default withRouter(function Main(props) {
  const [posts, setPosts] = useState(null);
  useEffect(() => {
    (async () => {
      try {
        setPosts(await getPosts());
      } catch {
        alert('문제가 발생했습니다. 관리자에게 문의해주세요.');
      }
    })();
  }, []);

  return posts ? (
    <Wrapper>
      <Header>
        <NavigationBarRoot>
          <Logo text="POCS"/>
          <NavigationBarList>
            <NavigationBarButton text="Board 1" to="board"/>
            <AccountButton/>
            <SearchButton/>
          </NavigationBarList>
        </NavigationBarRoot>
        <HeaderContent>
          <HeaderContentTitle>POCS Official</HeaderContentTitle>
          <HeaderContentText>Pioneer Of Computer Science</HeaderContentText>
        </HeaderContent>
      </Header>
      <Section>
        <NoticeBar text="Placeholder" date="2021.02.04"/>
      </Section>
      <Section>
        <Article>
          <ArticleTitleButton text="Board 1" to="board"/>
          {posts.map((post) => (
            <ArticleRow
              key={post.id}
              title={post.title}
              date={formatDate(new Date(post.created_at))}
              to={`/post/${post.id}`}
            />
          ))}
        </Article>
      </Section>
    </Wrapper>
  ) : (
   <Backdrop open />
  );
});
