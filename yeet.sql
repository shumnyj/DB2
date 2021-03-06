PGDMP                         w           testpost    10.6    11.2 $               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                       false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                       false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                       false                       1262    24576    testpost    DATABASE     �   CREATE DATABASE testpost WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Russian_Ukraine.1251' LC_CTYPE = 'Russian_Ukraine.1251';
    DROP DATABASE testpost;
             postgres    false                       0    0    DATABASE testpost    COMMENT     *   COMMENT ON DATABASE testpost IS 'lab db';
                  postgres    false    2842            �            1255    24708 	   pubauth()    FUNCTION     �  CREATE FUNCTION public.pubauth() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    au authors%rowtype;
	n integer;
	b integer;
BEGIN
	n = floor(random() * 5 + 1)::int;
    WHILE n>0 LOOP
        IF (n % 2) <> 0 THEN
			b = floor(random() * 20 + 3)::int;
		ELSE 
			b = 0;
		END IF;
		INSERT INTO authors(fname,sname,exp, written, publisher) 
		VALUES (n::text||'fname'||NEW.pname, n::text||'sname'||NEW.pname, 1, b, NEW.pname);
		n = n-1;
    END LOOP;
	RETURN NEW;
END;
$$;
     DROP FUNCTION public.pubauth();
       public       postgres    false            �            1255    24704 	   rebrand()    FUNCTION       CREATE FUNCTION public.rebrand() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    au authors%rowtype;
	bk books%rowtype;
BEGIN
    FOR au IN
        SELECT * FROM authors WHERE publisher = OLD.pname
    LOOP
        IF au.written > 0 THEN
			UPDATE authors SET publisher=NEW.pname WHERE (fname = au.fname) AND (sname = au.sname);
		ELSE 
			DELETE FROM authors WHERE (fname = au.fname) AND (sname = au.sname);
		END IF;
    END LOOP;
	FOR bk IN
        SELECT * FROM books WHERE pub = OLD.pname
    LOOP
        IF exists(SELECT * FROM authors WHERE (fname = bk.author_fname) AND (sname= bk.author_sname)) THEN
			UPDATE books SET pub=NEW.pname WHERE (barcode = r.barcode);
		ELSE 
			DELETE FROM books WHERE (barcode = bk.barcode);
		END IF;
	END LOOP;
END
$$;
     DROP FUNCTION public.rebrand();
       public       postgres    false            �            1255    24712 @   yreport(character varying, character varying, character varying)    FUNCTION       CREATE FUNCTION public.yreport(fn character varying, sn character varying, pb character varying) RETURNS integer
    LANGUAGE plpgsql
    AS $$
DECLARE
    bk books%rowtype;
	n integer;
BEGIN
	n=0;
	FOR bk in SELECT * FROM books WHERE author_fname=fn AND author_sname=sn
	LOOP
		IF bk.pub = pb THEN
			n=n+1;
		END IF;	
    END LOOP;
	IF n = 0 AND ((SELECT publisher FROM authors WHERE fname =fn AND sname = sn) = pb) THEN
		UPDATE authors SET publisher = NULL WHERE fname = fn AND sname = sn;
	END IF;
    RETURN n;
END
$$;
 `   DROP FUNCTION public.yreport(fn character varying, sn character varying, pb character varying);
       public       postgres    false            �            1259    24685 	   addresses    TABLE     ~   CREATE TABLE public.addresses (
    id integer NOT NULL,
    email_address character varying NOT NULL,
    user_id integer
);
    DROP TABLE public.addresses;
       public         shumnyj    false            �            1259    24683    addresses_id_seq    SEQUENCE     �   CREATE SEQUENCE public.addresses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.addresses_id_seq;
       public       shumnyj    false    202                       0    0    addresses_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.addresses_id_seq OWNED BY public.addresses.id;
            public       shumnyj    false    201            �            1259    24586    authors    TABLE     �   CREATE TABLE public.authors (
    fname character varying(32) NOT NULL,
    sname character varying(32) NOT NULL,
    exp integer,
    written integer,
    publisher character varying(64)
);
    DROP TABLE public.authors;
       public         shumnyj    false            �            1259    24578    books    TABLE     �   CREATE TABLE public.books (
    title character varying(64),
    pages integer,
    barcode integer NOT NULL,
    printing boolean,
    author_fname character varying(32),
    author_sname character varying(32),
    pub character varying(64)
);
    DROP TABLE public.books;
       public         shumnyj    false            �            1259    24583 
   publishers    TABLE     �   CREATE TABLE public.publishers (
    pname character varying(64) NOT NULL,
    address character varying(100),
    publ integer,
    director character varying(64)
);
    DROP TABLE public.publishers;
       public         shumnyj    false            �            1259    24677    users    TABLE     �   CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying(50),
    fullname character varying(50),
    nickname character varying(50)
);
    DROP TABLE public.users;
       public         shumnyj    false            �            1259    24675    users_id_seq    SEQUENCE     �   CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.users_id_seq;
       public       shumnyj    false    200                       0    0    users_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
            public       shumnyj    false    199            �
           2604    24688    addresses id    DEFAULT     l   ALTER TABLE ONLY public.addresses ALTER COLUMN id SET DEFAULT nextval('public.addresses_id_seq'::regclass);
 ;   ALTER TABLE public.addresses ALTER COLUMN id DROP DEFAULT;
       public       shumnyj    false    202    201    202            �
           2604    24680    users id    DEFAULT     d   ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
 7   ALTER TABLE public.users ALTER COLUMN id DROP DEFAULT;
       public       shumnyj    false    200    199    200                      0    24685 	   addresses 
   TABLE DATA                     public       shumnyj    false    202   	+                 0    24586    authors 
   TABLE DATA                     public       shumnyj    false    198   #+                 0    24578    books 
   TABLE DATA                     public       shumnyj    false    196   �+                 0    24583 
   publishers 
   TABLE DATA                     public       shumnyj    false    197   �,                 0    24677    users 
   TABLE DATA                     public       shumnyj    false    200   -                  0    0    addresses_id_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.addresses_id_seq', 14, true);
            public       shumnyj    false    201                       0    0    users_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.users_id_seq', 29, true);
            public       shumnyj    false    199            �
           2606    24693    addresses addresses_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);
 B   ALTER TABLE ONLY public.addresses DROP CONSTRAINT addresses_pkey;
       public         shumnyj    false    202            �
           2606    24590    authors authors_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.authors
    ADD CONSTRAINT authors_pkey PRIMARY KEY (fname, sname);
 >   ALTER TABLE ONLY public.authors DROP CONSTRAINT authors_pkey;
       public         shumnyj    false    198    198            �
           2606    24582    books book_pkey 
   CONSTRAINT     R   ALTER TABLE ONLY public.books
    ADD CONSTRAINT book_pkey PRIMARY KEY (barcode);
 9   ALTER TABLE ONLY public.books DROP CONSTRAINT book_pkey;
       public         shumnyj    false    196            �
           2606    24592    publishers publishers_pkey 
   CONSTRAINT     [   ALTER TABLE ONLY public.publishers
    ADD CONSTRAINT publishers_pkey PRIMARY KEY (pname);
 D   ALTER TABLE ONLY public.publishers DROP CONSTRAINT publishers_pkey;
       public         shumnyj    false    197            �
           2606    24682    users users_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public         shumnyj    false    200            �
           2620    24709    publishers pubtrig    TRIGGER     j   CREATE TRIGGER pubtrig AFTER INSERT ON public.publishers FOR EACH ROW EXECUTE PROCEDURE public.pubauth();
 +   DROP TRIGGER pubtrig ON public.publishers;
       public       shumnyj    false    197    217            �
           2606    24694     addresses addresses_user_id_fkey    FK CONSTRAINT        ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);
 J   ALTER TABLE ONLY public.addresses DROP CONSTRAINT addresses_user_id_fkey;
       public       shumnyj    false    200    202    2701            �
           2606    24593    books author    FK CONSTRAINT     �   ALTER TABLE ONLY public.books
    ADD CONSTRAINT author FOREIGN KEY (author_sname, author_fname) REFERENCES public.authors(sname, fname) MATCH FULL;
 6   ALTER TABLE ONLY public.books DROP CONSTRAINT author;
       public       shumnyj    false    2699    198    198    196    196            �
           2606    24603    books book_pub_fkey    FK CONSTRAINT     v   ALTER TABLE ONLY public.books
    ADD CONSTRAINT book_pub_fkey FOREIGN KEY (pub) REFERENCES public.publishers(pname);
 =   ALTER TABLE ONLY public.books DROP CONSTRAINT book_pub_fkey;
       public       shumnyj    false    2697    197    196            �
           2606    24598    authors publisher    FK CONSTRAINT     �   ALTER TABLE ONLY public.authors
    ADD CONSTRAINT publisher FOREIGN KEY (publisher) REFERENCES public.publishers(pname) MATCH FULL;
 ;   ALTER TABLE ONLY public.authors DROP CONSTRAINT publisher;
       public       shumnyj    false    198    2697    197               
   x���             �   x���M�@�ỿbn[ ���Qt��A���&EA���og�Eo.^��00�ez� +�=t��~kWM����
���NKX�˳y�Q� �P�@��t(�[/��$V�J4B�Y�+�����e�I����3R�l�;r�#G��8k'�F����8�8AƉ쵸�T�V�:ϝϥ�b%
���/���         �   x����
�@��>�ܶ`	gfՕN<a��]C!����o�`A�`�a������,O��Yq�~���eSu�m��nJrX	{���"	:
5!���l�Z�h彶o1��G��z�"3 
?f;^�щɉ����be &�4 VL��oj4 ��	�5��s3:3��F` ��N�����e�{~�{y         d   x���v
Q���W((M��L�S��E�
a�>���
���:
�)E ��� �I�r4��<�4�j�62��`D�	�P@����1�F�F`�pq �9T         
   x���         