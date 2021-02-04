import React, {useState}  from 'react';
import {Link, withRouter} from 'react-router-dom';
import styled             from 'styled-components';

const Wrapper = styled.main`
  margin:           0px;
  background-color: #eee;
  height:           100%;
`;

const Header = styled.header`
  display:          inline-block;
  width:            100%;
  height:           300px;
  background-color: darkblue;
`;

const HeaderContent = styled.div`
  text-align:       left;
  font-size:        24px;
  color:            white;
  padding-left:     80px;
  padding-top:      120px;
`

const LogoText = styled.div`
  display:          inline-block;
  float:            left;
  margin:           15px;
  margin-right:     20px;
  line-height:      30px;
  vertical-align:   middle;
  font-size:        28px;
  font-weight:      bold;
  color:            white;
`

const NavigationBarRoot = styled.nav`
  float:            right;
`

const NavigationBarList = styled.ul`
  list-style-type:  none;
  display:          inline-block;
  margin:           5px;
  overflow:         hidden;
`

const NavigationBarItem = styled.li`
  font-size:        14px;
  line-height:      30px;
  margin:           10px;
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
  margin:           40px 10px 10px 10px;
`

const Article = styled.article`
  margin:           20px;
`

const ArticleTitle = styled.h1`
  font-size:        16px;
  margin:           30px 40px 30px 40px;
`

const ArticleRowWrapper = styled.div`
  margin:           10px 40px 10px 40px;
  padding:          10px;
  background-color: white;
  text-decoration:  none;
`

const ArticleRowTitle = styled.span`
  font-weight:      bold;
  margin:           5px 5px 0px 0px;
  font-size:        14px;
`

const ArticleRowDate = styled.span`
  float:            right;
  font-size:        14px;
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

export default withRouter(function Board(props) {
  return (
    <Wrapper>
      <Header>
        <Logo text="POCS"/>
        <NavigationBarRoot>
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
        <Article>
          <ArticleTitle>최근 게시글</ArticleTitle>
          <ArticleRow title="Title 1" date="2021.02.04" to="post"/>
          <ArticleRow title="Title 2" date="2021.02.04" to="post"/>
          <ArticleRow title="Title 3" date="2021.02.04" to="post"/>
          <ArticleRow title="Title 4" date="2021.02.04" to="post"/>
          <ArticleRow title="Title 5" date="2021.02.04" to="post"/>
        </Article>
      </Section>
    </Wrapper>
  );
});
