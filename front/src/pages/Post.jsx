import React, {useState}  from 'react';
import {Link, withRouter} from 'react-router-dom';
import styled             from 'styled-components';

const Wrapper = styled.main`
  margin:           0px;
  background-color: white;
  height:           100%;
`;

const Header = styled.header`
  display:          inline-block;
  width:            100%;
  min-height:       300px;
  background-color: black;
`;

const HeaderContent = styled.div`
  text-align:       left;
  font-size:        24px;
  color:            white;
  padding-left:     40px;
  padding-right:    40px;
  padding-top:      100px;

  margin:           auto;
  margin-top:       40px;
  margin-bottom:    60px;
  max-width:        1024px;
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
  margin-bottom:    30px;
`

const HeaderContentDate = styled.p`
  font-size:        16px;
  color:            lightgray;
  margin-bottom:    40px;
`

const Section = styled.section`
  margin:           auto;
  max-width:        1024px;
  padding:          40px;
  background-color: white;
`

const Article = styled.article`
  margin:           0px;
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

export default withRouter(function Post(props) {
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
          <HeaderContentTitle>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit.
          </HeaderContentTitle>
          <HeaderContentDate>2020.02.04</HeaderContentDate>
        </HeaderContent>
      </Header>
      <Section>
        <Article>
          <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec feugiat, turpis ut tempor elementum, felis felis mollis elit, eget fermentum nisl diam nec felis. Vivamus in consectetur nunc. Nunc tincidunt lectus sit amet mauris convallis, non imperdiet nunc malesuada. Aenean nisi leo, bibendum ut lectus nec, sollicitudin efficitur justo. Integer commodo ante eros, at dictum diam eleifend ac. Maecenas scelerisque lorem interdum, dignissim magna id, tempus libero. Aenean molestie nulla id metus tempor, at fringilla leo finibus. Praesent efficitur diam ac ipsum accumsan venenatis. Suspendisse potenti. Vivamus lectus magna, lacinia id faucibus ac, pulvinar ac magna. In ultrices, magna ac porttitor porttitor, est dolor venenatis ante, non scelerisque orci urna sodales tellus. Praesent id pulvinar purus. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Morbi aliquam ut nisl consectetur lobortis.

Nullam ac lacus turpis. Ut mollis odio id nisl porttitor dignissim. Duis vulputate nisi scelerisque tellus tincidunt, id ultricies eros tempus. Aenean eget elit tristique, pharetra turpis sit amet, sodales mi. Phasellus rutrum eros sed mattis mattis. Integer faucibus erat et malesuada faucibus. Maecenas feugiat suscipit felis a eleifend. Sed molestie, quam feugiat vehicula euismod, sem libero iaculis nunc, quis suscipit lectus erat sit amet felis. Morbi sit amet tristique elit. Donec feugiat libero dui, quis blandit lectus condimentum vel. Nulla vehicula ullamcorper mauris. Aliquam lacinia nulla sed tellus ultricies, nec elementum nisi posuere. Duis purus ipsum, venenatis eget lacus eget, tincidunt consequat purus. Praesent rutrum ex vestibulum, suscipit tellus nec, bibendum orci.

Cras iaculis consequat maximus. Nullam at rutrum magna. Ut a rhoncus nunc. Vivamus mollis tortor ut libero pulvinar ornare. Aliquam id velit feugiat, aliquam tortor vel, imperdiet metus. Nunc vel eros consequat, fringilla mi ut, porta eros. Phasellus at consectetur est. Maecenas quam mauris, interdum at ultricies tempor, bibendum vulputate eros. In cursus dictum nibh, a elementum libero rutrum nec. Nunc non risus in turpis maximus viverra lobortis id odio. Donec vel fringilla ante. Quisque consectetur ipsum sodales, auctor mauris quis, ullamcorper nisl. Donec in mattis ipsum. Pellentesque eget risus non lectus ultrices dignissim in vitae velit. Vivamus molestie diam et nisl bibendum finibus.

Quisque nec elit fringilla, tristique enim semper, venenatis eros. Mauris eu tempus nibh. Donec eget convallis diam. Fusce aliquet lectus vel ex pulvinar pharetra. Etiam bibendum malesuada libero pulvinar egestas. Sed bibendum pretium gravida. Morbi consectetur orci lacus, sit amet pharetra metus iaculis nec. Ut congue non eros consectetur viverra. Sed quis interdum augue. Aenean vel aliquet turpis, quis tincidunt ligula. Suspendisse nec diam pretium, ornare massa ut, posuere ipsum. Quisque non maximus sapien. Nulla viverra diam a nisl rhoncus, sit amet posuere tortor rhoncus.

Integer molestie mollis ipsum quis porta. Maecenas sollicitudin porttitor dui, vel aliquam augue convallis in. Proin quis libero nulla. Sed maximus risus nunc, sed consectetur sapien fermentum nec. Sed odio orci, finibus in venenatis sit amet, tincidunt a odio. Ut in dignissim ante. Fusce maximus lacus nec nisl interdum, in consequat enim sagittis. Aliquam tincidunt urna interdum lacus facilisis congue. Phasellus rutrum dui erat, eget rutrum neque pharetra quis. Integer tempor placerat venenatis. Cras hendrerit malesuada massa, eu porttitor nulla aliquet vitae. Pellentesque ut finibus neque. Nam tincidunt fringilla sapien, sed hendrerit tortor venenatis ac. Nunc condimentum orci a ipsum egestas, nec posuere orci maximus. Etiam nec est est.

Quisque bibendum congue nulla a pulvinar. Aenean eget risus vulputate est sodales rhoncus. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Maecenas tempus venenatis lacus, non bibendum neque semper non. Donec nec eros at urna imperdiet imperdiet non vitae massa. Proin non velit a arcu fringilla commodo vel ut neque. Maecenas tincidunt augue leo, quis varius urna placerat non.

Phasellus ut pellentesque lectus. Morbi dictum nulla at sollicitudin vestibulum. Cras elementum, nibh ut porttitor feugiat, justo augue dictum nunc, sit amet malesuada nisi eros id leo. Curabitur hendrerit eu eros et gravida. Aenean sapien tellus, maximus viverra viverra id, tempus sed velit. Mauris luctus tristique metus, nec sollicitudin eros facilisis eget. Fusce et interdum neque, eget faucibus nulla. Sed est ligula, dapibus quis lacinia ac, hendrerit non mi. In luctus at urna a condimentum. Integer at quam eget leo hendrerit tempus. Donec sed porttitor sapien. Praesent dictum maximus tellus nec congue. Phasellus ac aliquet sapien. Nullam sit amet nisi lacus.

Donec libero quam, eleifend pulvinar ipsum nec, consectetur cursus diam. Ut suscipit, velit eget lacinia gravida, sapien magna venenatis ligula, ut malesuada dui augue a arcu. Phasellus aliquam sagittis sapien et congue. Duis convallis nisi vitae ipsum consequat, ut varius orci consectetur. Maecenas porta, augue vitae elementum euismod, ligula sem feugiat velit, eu bibendum erat ligula sed nunc. Vivamus suscipit venenatis sollicitudin. Mauris commodo convallis ex non lacinia. Curabitur condimentum vestibulum felis, non lobortis lacus commodo at. Etiam neque orci, mattis nec tellus non, maximus gravida urna. Integer vitae augue ut orci iaculis egestas eget in velit. Quisque accumsan nec velit quis viverra. Mauris pharetra nulla in urna laoreet, a iaculis tortor aliquam.

Morbi in nisi ut tellus semper vestibulum tristique sit amet odio. Praesent faucibus pellentesque nulla rhoncus ultrices. Praesent vel libero lorem. Ut et ligula ut massa bibendum auctor vitae eget nunc. Nulla accumsan sed mi quis aliquam. Nullam tempor augue at purus lobortis vestibulum. Praesent id lectus scelerisque, accumsan justo id, sagittis ligula. Integer maximus urna sem, at consectetur massa viverra pellentesque. Aliquam rutrum ante ut iaculis aliquam. Aliquam vel metus ac est congue finibus. Fusce sed risus eget massa consequat ultricies et efficitur leo. Phasellus cursus, velit vel suscipit maximus, nisl ante suscipit augue, egestas commodo mi nisi sit amet erat. Suspendisse potenti. Ut egestas pellentesque auctor. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Nulla et nisi at velit pulvinar faucibus vitae nec tellus.

Vivamus lacinia, mi ac consectetur condimentum, dui velit accumsan tortor, a pulvinar tellus elit vitae massa. In eu dictum nisl, eu rutrum arcu. Sed semper et tellus eu mattis. In imperdiet aliquet congue. Aenean viverra ex vitae vehicula ultricies. Sed lectus diam, pretium in ipsum ac, ultrices auctor dolor. Praesent eget malesuada leo.
          </p>
        </Article>
      </Section>
    </Wrapper>
  );
});
