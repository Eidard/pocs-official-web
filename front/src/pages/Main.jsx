import React, {useState} from 'react';
import { Link, withRouter } from 'react-router-dom';
import styled from 'styled-components';

const Wrapper = styled.main`
  margin: 0px;
  background-color: #eee;
  height: 100%;
`;

const Header = styled.header`
  display: inline-block;
  width: 100%;
  height: 300px;
  background-color: darkblue;
`;

const HeaderContent = styled.div`
  text-align: left;
  font-size: 24px;
  color: white;
  padding-left: 80px;
  padding-top: 120px;
`

const Logo = styled.div`
  display : inline-block;
  float : left;

  margin: 15px;
  margin-right : 20px;

  line-height: 30px;
  vertical-align: middle;

  font-size: 28px;
  font-weight: bold;

  color: white;

`

const NavigationBarRoot = styled.nav`
  float: right;
`

const NavigationBarList = styled.ul`
  list-style-type: none;
  display : inline-block;
  margin: 5px;
  overflow: hidden;
`

const NavigationBarItem = styled.li`
  font-size: 14px;
  line-height: 30px;
  margin: 10px;
  margin-left: 16px;
  margin-right: 16px;
  display : inline-block;
  vertical-align: middle;
  text-decoration: none;
  color : white;
`

const NavigationBarImageItem = styled.img`
  width: 20px;
  height: 20px;
  margin-left: 16px;
  margin-right: 16px;
  filter: invert(1);
  vertical-align: middle;
`

const HeaderContentTitle = styled.p`
  font-size: 40px;
  font-weight: bold;
  margin-bottom: 10px;
`

const HeaderContentText = styled.p`
  font-size: 16px;
  color: lightgray;
`
const Section = styled.section`
  margin: 20px 40px 20px 40px;
  padding: 10px;
  background-color: white;
`

const Article = styled.article`
  margin: 10px 10px 10px 10px;
`

const NoticeBarTitle = styled.span`
  font-weight: bold;
  margin-right: 10px;
  font-size: 16px;
`

const NoticeBarText = styled.span`
  font-size: 14px;
`

const NoticeBarDate = styled.span`
  float: right;
  font-size: 14px;
`

const NoticeBar = (props) => {
  return(
    <Section>
      <Article>
        <NoticeBarTitle>공지사항</NoticeBarTitle>
        <NoticeBarText>{ props.text }</NoticeBarText>
        <NoticeBarDate>{ props.date }</NoticeBarDate>
      </Article>
  </Section>
  );
}



const AccountButton = () => {
  return <Link to="/login"><NavigationBarImageItem src="/images/main/account.png"/></Link>
}

const SearchButton = () => {
  return <NavigationBarImageItem src="/images/main/search.png"/>
}

const ArticleTitle = styled.h1`
  font-size: 16px;
  margin-bottom: 20px;
`

const ArticleRowWrapper = styled.div`
  margin-bottom: 5px;
`

const ArticleRowTitle = styled.span`
  margin: 5px 5px 0px 0px;
  font-size: 14px;
`

const ArticleRowText = styled.span`
  margin: 5px 5px 0px 0px;
  font-size: 14px;
`

const ArticleRowDate = styled.span`
  float: right;
  font-size: 14px;
`

const ArticleRow = (props) => {
  return(
    <ArticleRowWrapper>
      <ArticleRowTitle>{ props.title }</ArticleRowTitle>
      <ArticleRowDate>{ props.date }</ArticleRowDate>
    </ArticleRowWrapper>
  );
}

export default withRouter(function Main(props) {
  return (
    <Wrapper>
      <Header>
        <Logo>POCS</Logo>
        <NavigationBarRoot>
          <NavigationBarList>
            <NavigationBarItem>Board 1</NavigationBarItem>
            <AccountButton/>
            <SearchButton/>
          </NavigationBarList>
        </NavigationBarRoot>
        <HeaderContent>
          <HeaderContentTitle>POCS Official</HeaderContentTitle>
          <HeaderContentText>Pioneer Of Computer Science</HeaderContentText>
        </HeaderContent>
      </Header>
      <NoticeBar text="Placeholder" date="2021.02.04"/>
      <Section>
        <Article>
          <ArticleTitle>Board 1</ArticleTitle>
          <ArticleRow title="Title 1" date="2021.02.04"/>
          <ArticleRow title="Title 2" date="2021.02.04"/>
          <ArticleRow title="Title 3" date="2021.02.04"/>
          <ArticleRow title="Title 4" date="2021.02.04"/>
          <ArticleRow title="Title 5" date="2021.02.04"/>
        </Article>
      </Section>
    </Wrapper>
  );
});
