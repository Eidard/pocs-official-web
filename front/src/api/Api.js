// const HOST = 'http://52.78.88.64';
const HOST = 'http://localhost:8000';

export function generateUrl(path) {
  return `${HOST}${path}/`;
}

export async function requestRegister(
  studentId,
  name,
  email,
  username,
  password,
  birth,
  gender,
  phone,
  joinedYear
) {
  const response = await fetch(generateUrl('/users'), {
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: "include",
    body: JSON.stringify({
      student_id: studentId,
      name,
      email,
      username,
      password,
      birth,
      gender,
      phone,
      generation: joinedYear,
    }),
  });

  if (!response.ok) throw response;
}

export async function authenticate(username, password) {
  const response = await fetch(generateUrl('/users/sessions'), {
    method: 'post',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: "include",
    body: JSON.stringify({
      username,
      password,
    }),
  });

  if (!response.ok) throw response;
}

export async function getPosts() {
  const response = await fetch(generateUrl('/posts'), {
    method: 'get',
    credentials: "include",
  });

  if (!response.ok) throw response;

  return await response.json();
}

export async function getPost(id) {
  const response = await fetch(generateUrl(`/posts/${id}`), {
    method: 'get',
  });

  if (!response.ok) throw response;

  return await response.json();
}
